#!/usr/bin/env python3
"""Inspect and migrate Codex projects to the current project structure."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import date, datetime
import json
from pathlib import Path
import re
import shutil
import sys
from typing import Any

from manager_common import (
    MANAGER_VERSION,
    PROJECT_SCHEMA,
    PROJECT_SCHEMA_VERSION,
    ManagerError,
    atomic_write_json,
    atomic_write_text,
    default_config_file,
    load_config,
    validate_roots,
)


REQUIRED_DIRECTORIES = (
    "attachments",
    "screenshots",
    "configs",
    "presentations",
    "logs",
    "plans",
)
REQUIRED_FILES = (
    "NOTES.md",
    "plans/REQUIREMENTS.md",
    "plans/WORKFLOW.md",
    "plans/CHECKLIST.md",
    "plans/TRACEABILITY.md",
    "plans/STATUS.md",
    "plans/DECISIONS.md",
    "logs/LOG_TEMPLATE.md",
)
STATUS_HEADINGS = (
    "Last Updated",
    "Current State",
    "Last Completed",
    "Next Action",
    "Blocked By",
)


@dataclass
class ProjectPlan:
    root: Path
    classification: str
    schema_version: int | None = None
    project_name: str | None = None
    actions: list[str] = field(default_factory=list)
    error: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate Codex project structures.")
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument(
        "--all", action="store_true", help="Inspect all workspace projects"
    )
    selection.add_argument("--project", help="Inspect one immediate workspace child")
    parser.add_argument(
        "--apply", action="store_true", help="Apply the planned migrations"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Show detailed planned actions"
    )
    parser.add_argument("--config-file", type=Path, default=default_config_file())
    parser.add_argument(
        "--workspace", type=Path, help="Override configured workspace for testing"
    )
    parser.add_argument(
        "--manager-root", type=Path, help="Override manager root for testing"
    )
    return parser.parse_args()


def _safe_child(workspace: Path, name: str) -> Path:
    if not name or name in {".", ".."} or Path(name).name != name:
        raise ManagerError(f"Project must be one immediate workspace child: {name!r}")
    candidate = workspace / name
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(workspace.resolve())
    except ValueError as exc:
        raise ManagerError(f"Project path escapes workspace: {name}") from exc
    if candidate.is_symlink():
        raise ManagerError(f"Project symlinks are not supported: {candidate}")
    return candidate


def _read_identity(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ManagerError(f"Invalid project identity {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ManagerError(f"Project identity must be a JSON object: {path}")
    return data


def _status_missing_headings(status_file: Path) -> list[str]:
    if not status_file.is_file():
        return []
    text = status_file.read_text(encoding="utf-8")
    present = set(re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE))
    return [heading for heading in STATUS_HEADINGS if heading not in present]


def inspect_project(project: Path) -> ProjectPlan:
    if project.is_symlink():
        return ProjectPlan(
            project, "conflicting", error="Project symlinks are not supported"
        )
    if not project.is_dir() or project.name.startswith("."):
        return ProjectPlan(project, "unrelated")

    identity_file = project / ".codex-project.json"
    notes = project / "NOTES.md"
    status = project / "plans" / "STATUS.md"

    if identity_file.exists():
        try:
            identity = _read_identity(identity_file)
            if identity.get("schema") != PROJECT_SCHEMA:
                raise ManagerError(f"Unexpected schema: {identity.get('schema')!r}")
            if identity.get("project_folder") != project.name:
                raise ManagerError(
                    f"project_folder {identity.get('project_folder')!r} does not match {project.name!r}"
                )
            schema_version = identity.get("schema_version", identity.get("version"))
            if (
                isinstance(schema_version, bool)
                or not isinstance(schema_version, int)
                or schema_version < 1
            ):
                raise ManagerError(f"Invalid schema_version: {schema_version!r}")
            if schema_version > PROJECT_SCHEMA_VERSION:
                raise ManagerError(
                    f"Project schema_version {schema_version} is newer than supported {PROJECT_SCHEMA_VERSION}"
                )
            project_name = identity.get("project_name")
            if not isinstance(project_name, str) or not project_name:
                raise ManagerError("project_name must be a nonempty string")
            manager_version = identity.get("manager_version")
        except ManagerError as exc:
            return ProjectPlan(project, "conflicting", error=str(exc))
        classification = (
            "current" if schema_version == PROJECT_SCHEMA_VERSION else "legacy"
        )
        plan = ProjectPlan(project, classification, schema_version, project_name)
        if "schema_version" not in identity or "version" in identity:
            plan.actions.append(f"set schema_version {PROJECT_SCHEMA_VERSION}")
        if manager_version != MANAGER_VERSION:
            plan.actions.append(f"set manager version {MANAGER_VERSION}")
    elif notes.is_file():
        plan = ProjectPlan(project, "legacy", 0, project.name)
        plan.actions.append("create .codex-project.json")
    elif status.exists():
        return ProjectPlan(
            project,
            "conflicting",
            error="plans/STATUS.md exists without NOTES.md",
        )
    else:
        return ProjectPlan(project, "unrelated")

    for relative in REQUIRED_DIRECTORIES:
        target = project / relative
        if target.is_symlink():
            return ProjectPlan(
                project, "conflicting", error=f"Symlink not supported: {relative}"
            )
        if not target.exists():
            plan.actions.append(f"create directory {relative}")
        elif not target.is_dir():
            return ProjectPlan(
                project, "conflicting", error=f"Expected directory: {relative}"
            )

    for relative in REQUIRED_FILES:
        target = project / relative
        if target.is_symlink():
            return ProjectPlan(
                project, "conflicting", error=f"Symlink not supported: {relative}"
            )
        if not target.exists():
            plan.actions.append(f"create file {relative}")
        elif not target.is_file():
            return ProjectPlan(
                project, "conflicting", error=f"Expected file: {relative}"
            )

    try:
        for heading in _status_missing_headings(status):
            plan.actions.append(f"add STATUS heading {heading}")
    except (OSError, UnicodeError) as exc:
        return ProjectPlan(
            project, "conflicting", error=f"Unable to read STATUS.md: {exc}"
        )

    if plan.schema_version and plan.schema_version != PROJECT_SCHEMA_VERSION:
        plan.actions.append(f"set schema_version {PROJECT_SCHEMA_VERSION}")
    if plan.actions and plan.classification == "current":
        plan.classification = "legacy"
    return plan


def _load_skeletons(manager_root: Path) -> dict[str, str]:
    source = manager_root / "PROJECT_FILE_SKELETONS.md"
    try:
        text = source.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ManagerError(f"Unable to read skeletons {source}: {exc}") from exc

    sections: dict[str, str] = {}
    pattern = re.compile(
        r"^## `([^`]+)`\s*\n+```(?:json|markdown)?\s*\n(.*?)^```\s*$",
        re.MULTILINE | re.DOTALL,
    )
    for match in pattern.finditer(text):
        sections[match.group(1)] = match.group(2).rstrip() + "\n"
    missing = [path for path in REQUIRED_FILES if path not in sections]
    if missing:
        raise ManagerError("Skeleton file is missing sections: " + ", ".join(missing))
    return sections


def _render_skeleton(template: str, project_name: str, folder: str) -> str:
    rendered = template.replace("{Project Name}", project_name)
    rendered = rendered.replace("{project folder name}", folder)
    rendered = rendered.replace("{YYYY-MM-DD}", date.today().isoformat())
    rendered = re.sub(r"\{[^{}]+\}", "To be determined", rendered)
    return rendered


def _identity_for(plan: ProjectPlan) -> dict[str, Any]:
    identity_file = plan.root / ".codex-project.json"
    if identity_file.exists():
        identity = _read_identity(identity_file)
    else:
        identity = {
            "schema": PROJECT_SCHEMA,
            "project_name": plan.project_name or plan.root.name,
            "project_folder": plan.root.name,
            "created_at": date.today().isoformat(),
        }
    identity.pop("version", None)
    identity["schema_version"] = PROJECT_SCHEMA_VERSION
    identity["manager_version"] = MANAGER_VERSION
    identity["migrated_at"] = date.today().isoformat()
    return identity


def apply_plan(plan: ProjectPlan, manager_root: Path, backup_root: Path) -> None:
    if plan.classification != "legacy" or not plan.actions:
        return

    skeletons = _load_skeletons(manager_root)
    project_backup = backup_root / plan.root.name
    project_backup.mkdir(parents=True, exist_ok=False)
    created_files: list[Path] = []
    created_dirs: list[Path] = []
    modified_files: list[tuple[Path, Path]] = []

    def backup_file(target: Path) -> None:
        relative = target.relative_to(plan.root)
        destination = project_backup / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, destination)
        modified_files.append((target, destination))

    try:
        for relative in REQUIRED_DIRECTORIES:
            target = plan.root / relative
            if not target.exists():
                target.mkdir()
                created_dirs.append(target)

        for relative in REQUIRED_FILES:
            target = plan.root / relative
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                content = _render_skeleton(
                    skeletons[relative],
                    plan.project_name or plan.root.name,
                    plan.root.name,
                )
                atomic_write_text(target, content, backup=False)
                created_files.append(target)

        status = plan.root / "plans" / "STATUS.md"
        missing_headings = _status_missing_headings(status)
        if missing_headings:
            backup_file(status)
            text = status.read_text(encoding="utf-8").rstrip()
            additions = "".join(
                f"\n\n## {heading}\n\n- To be determined"
                for heading in missing_headings
            )
            atomic_write_text(status, text + additions + "\n", backup=False)

        identity_file = plan.root / ".codex-project.json"
        if identity_file.exists():
            backup_file(identity_file)
        else:
            created_files.append(identity_file)
        atomic_write_json(identity_file, _identity_for(plan), backup=False)
    except Exception as exc:
        for target, backup in reversed(modified_files):
            shutil.copy2(backup, target)
        for target in reversed(created_files):
            target.unlink(missing_ok=True)
        for target in reversed(created_dirs):
            try:
                target.rmdir()
            except OSError:
                pass
        raise ManagerError(
            f"Migration failed for {plan.root.name} and was rolled back: {exc}"
        ) from exc


def _workspace_and_manager(args: argparse.Namespace) -> tuple[Path, Path]:
    if args.workspace or args.manager_root:
        if not args.workspace or not args.manager_root:
            raise ManagerError("--workspace and --manager-root must be used together")
        manager, workspace = validate_roots(args.manager_root, args.workspace)
        return workspace, manager
    config = load_config(args.config_file)
    return config.workspace_root, config.manager_root


def _print_plan(plan: ProjectPlan) -> None:
    print(_plan_summary(plan))
    if plan.error:
        print(f"  error: {plan.error}")


def _print_plan_verbose(plan: ProjectPlan) -> None:
    print(_plan_summary(plan))
    if plan.error:
        print(f"  error: {plan.error}")
    for action in plan.actions:
        print(f"  - {action}")


def _legacy_backup_dirs(workspace: Path) -> list[Path]:
    pattern = f"{workspace.name}_legacy_template_backup_*"
    return sorted(
        path
        for path in workspace.parent.glob(pattern)
        if path.is_dir() and not path.is_symlink()
    )


def _remove_if_exists(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def _cleanup_backup_paths(workspace: Path) -> list[Path]:
    removed: list[Path] = []
    candidates = [
        workspace / ".codex-project-backups",
        workspace / ".codex-migration-reports",
    ]
    candidates.extend(_legacy_backup_dirs(workspace))
    for path in candidates:
        if path.exists():
            _remove_if_exists(path)
            removed.append(path)
    return removed


def _should_cleanup_backups() -> bool:
    if not sys.stdin.isatty():
        return False

    print("Delete migration backup files now?")
    print("1. Yes")
    print("2. No")
    try:
        answer = input("Select [1/2, default 2]: ").strip().lower()
    except EOFError:
        return False
    return answer in {"1", "y", "yes"}


def _plan_summary(plan: ProjectPlan) -> str:
    if plan.classification == "legacy" and plan.actions:
        return (
            f"[{plan.classification}] {plan.root.name}: "
            f"needs update, {len(plan.actions)} changes"
        )
    if plan.classification in {"unrelated", "conflicting"}:
        return f"[{plan.classification}] {plan.root.name}"
    if plan.classification == "current":
        return f"[{plan.classification}] {plan.root.name}: up to date"
    return f"[{plan.classification}] {plan.root.name}"


def main() -> int:
    args = parse_args()
    try:
        workspace, manager_root = _workspace_and_manager(args)
        if not workspace.is_dir():
            raise ManagerError(f"Workspace not found: {workspace}")
        if not manager_root.is_dir():
            raise ManagerError(f"Manager not found: {manager_root}")

        if args.project:
            projects = [_safe_child(workspace, args.project)]
            if not projects[0].is_dir():
                raise ManagerError(f"Project not found: {projects[0]}")
        else:
            projects = sorted(
                (
                    path
                    for path in workspace.iterdir()
                    if path.is_dir() and not path.name.startswith(".")
                ),
                key=lambda path: path.name.lower(),
            )

        plans = [inspect_project(project) for project in projects]
        for plan in plans:
            if args.verbose:
                _print_plan_verbose(plan)
            else:
                _print_plan(plan)

        conflicts = [plan for plan in plans if plan.classification == "conflicting"]
        migratable = [
            plan for plan in plans if plan.classification == "legacy" and plan.actions
        ]
        if conflicts:
            print(f"Conflicts: {len(conflicts)}", file=sys.stderr)
            return 2
        if not args.apply:
            print(f"Preview: {len(migratable)} project(s) would be migrated")
            return 0
        if not migratable:
            print("No project migrations required")
            return 0

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = workspace / ".codex-project-backups" / stamp
        backup_root.mkdir(parents=True, exist_ok=False)
        failures = 0
        for plan in migratable:
            try:
                apply_plan(plan, manager_root, backup_root)
                print(f"Migrated: {plan.root.name}")
            except ManagerError as exc:
                failures += 1
                print(f"Migration failed: {plan.root.name}: {exc}", file=sys.stderr)

        if failures:
            print(f"Backup: {backup_root}")
            return 2

        if _should_cleanup_backups():
            removed = _cleanup_backup_paths(workspace)
            print(f"Deleted backup path(s): {len(removed)}")
        else:
            print(f"Backup: {backup_root}")
        return 0
    except (ManagerError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
