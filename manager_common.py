#!/usr/bin/env python3
"""Shared configuration and file operations for codex_project_manager."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any


MANAGER_VERSION = "V4.1_260707"
CONFIG_SCHEMA = "codex_project_manager"
CONFIG_VERSION = 1
PROJECT_SCHEMA = "codex_projects"
PROJECT_SCHEMA_VERSION = 2

BEGIN_MARKER = "<!-- BEGIN CODEX_PROJECTS MANAGED INSTRUCTIONS -->"
END_MARKER = "<!-- END CODEX_PROJECTS MANAGED INSTRUCTIONS -->"
MANAGED_BLOCK = re.compile(
    rf"(?:\n*){re.escape(BEGIN_MARKER)}.*?{re.escape(END_MARKER)}(?:\n*)",
    re.DOTALL,
)

REQUIRED_MANAGER_FILES = (
    "AGENTS_REQ.md",
    "PROJECT_CREATION_RUNBOOK.md",
    "PROJECT_FILE_SKELETONS.md",
    "setup.py",
    "migrate_projects.py",
    "manager_common.py",
)


class ManagerError(RuntimeError):
    """Raised when manager configuration or file state is unsafe."""


@dataclass(frozen=True)
class ManagerConfig:
    manager_root: Path
    workspace_root: Path
    installed_version: str = MANAGER_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": CONFIG_SCHEMA,
            "config_version": CONFIG_VERSION,
            "manager_root": str(self.manager_root),
            "workspace_root": str(self.workspace_root),
            "installed_version": self.installed_version,
        }


def default_config_file() -> Path:
    return Path.home() / ".codex" / "codex-projects.json"


def default_agents_file() -> Path:
    return Path.home() / ".codex" / "AGENTS.md"


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def _is_nested(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validate_roots(manager_root: Path, workspace_root: Path) -> tuple[Path, Path]:
    manager = _resolved(manager_root)
    workspace = _resolved(workspace_root)

    if manager == workspace:
        raise ManagerError("Manager and workspace roots must be different")
    if _is_nested(manager, workspace) or _is_nested(workspace, manager):
        raise ManagerError("Manager and workspace roots must not be nested")
    if not manager.is_dir():
        raise ManagerError(f"Manager directory not found: {manager}")

    missing = [
        name for name in REQUIRED_MANAGER_FILES if not (manager / name).is_file()
    ]
    if missing:
        raise ManagerError(
            "Manager directory is missing required files: " + ", ".join(missing)
        )
    return manager, workspace


def load_config(path: Path) -> ManagerConfig:
    config_path = _resolved(path)
    if not config_path.is_file():
        raise ManagerError(f"Configuration file not found: {config_path}")
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ManagerError(f"Invalid configuration file {config_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ManagerError(f"Configuration must contain a JSON object: {config_path}")
    if data.get("schema") != CONFIG_SCHEMA:
        raise ManagerError(f"Unexpected configuration schema: {data.get('schema')!r}")
    if data.get("config_version") != CONFIG_VERSION:
        raise ManagerError(
            f"Unsupported configuration version: {data.get('config_version')!r}"
        )
    for key in ("manager_root", "workspace_root", "installed_version"):
        if not isinstance(data.get(key), str) or not data[key]:
            raise ManagerError(f"Configuration key must be a nonempty string: {key}")

    manager, workspace = validate_roots(
        Path(data["manager_root"]), Path(data["workspace_root"])
    )
    return ManagerConfig(manager, workspace, data["installed_version"])


def _backup_path(path: Path) -> Path:
    return path.with_name(f"{path.name}.bak")


def atomic_write_text(path: Path, text: str, *, backup: bool = True) -> Path | None:
    target = _resolved(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    backup_path: Path | None = None
    temp_path: Path | None = None

    try:
        if backup and target.exists():
            backup_path = _backup_path(target)
            shutil.copy2(target, backup_path)

        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", newline="\n", dir=target.parent, delete=False
        ) as handle:
            handle.write(text)
            temp_path = Path(handle.name)

        if target.exists():
            os.chmod(temp_path, target.stat().st_mode)
        os.replace(temp_path, target)
        return backup_path
    except Exception:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise


def atomic_write_json(
    path: Path, data: dict[str, Any], *, backup: bool = True
) -> Path | None:
    serialized = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    return atomic_write_text(path, serialized, backup=backup)


def write_config(path: Path, config: ManagerConfig) -> Path | None:
    manager, workspace = validate_roots(config.manager_root, config.workspace_root)
    normalized = ManagerConfig(manager, workspace, config.installed_version)
    target = _resolved(path)
    existed = target.exists()
    backup = atomic_write_json(path, normalized.to_dict())
    try:
        reloaded = load_config(path)
        if reloaded != normalized:
            raise ManagerError(f"Configuration verification failed: {target}")
    except Exception:
        if backup and backup.exists():
            shutil.copy2(backup, target)
        elif not existed:
            target.unlink(missing_ok=True)
        raise
    return backup


def render_instructions(manager_root: Path, workspace_root: Path) -> str:
    source = manager_root / "AGENTS_REQ.md"
    try:
        rendered = source.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ManagerError(f"Unable to read instructions {source}: {exc}") from exc

    rendered = rendered.replace("<CODEX_PROJECT_MANAGER_ROOT>", str(manager_root))
    rendered = rendered.replace("<CODEX_PROJECTS_WORKSPACE_ROOT>", str(workspace_root))
    unresolved = sorted(set(re.findall(r"<CODEX_PROJECT[^>]*>", rendered)))
    if unresolved:
        raise ManagerError(
            "Unresolved instruction placeholders: " + ", ".join(unresolved)
        )
    return rendered.rstrip()


def install_managed_instructions(
    manager_root: Path, workspace_root: Path, agents_file: Path
) -> Path | None:
    manager, workspace = validate_roots(manager_root, workspace_root)
    target = _resolved(agents_file)
    try:
        existing = target.read_text(encoding="utf-8") if target.exists() else ""
    except (OSError, UnicodeError) as exc:
        raise ManagerError(f"Unable to read instruction file {target}: {exc}") from exc

    if existing.count(BEGIN_MARKER) != existing.count(END_MARKER):
        raise ManagerError(f"Managed instruction markers do not match in {target}")

    unmanaged = MANAGED_BLOCK.sub("\n", existing).rstrip()
    rendered = render_instructions(manager, workspace)
    managed = f"{BEGIN_MARKER}\n{rendered}\n{END_MARKER}"
    updated = f"{unmanaged}\n\n{managed}\n" if unmanaged else f"{managed}\n"
    existed = target.exists()
    backup = atomic_write_text(target, updated)

    try:
        verified = target.read_text(encoding="utf-8")
        if verified.count(BEGIN_MARKER) != 1 or verified.count(END_MARKER) != 1:
            raise ManagerError(f"Managed instruction verification failed: {target}")
        if str(manager) not in verified or str(workspace) not in verified:
            raise ManagerError(
                f"Installed paths were not found in instructions: {target}"
            )
    except Exception:
        if backup and backup.exists():
            shutil.copy2(backup, target)
        elif not existed:
            target.unlink(missing_ok=True)
        raise
    return backup
