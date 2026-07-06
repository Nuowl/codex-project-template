#!/usr/bin/env python3
"""Install or update codex_project_manager without touching project data."""

from __future__ import annotations

import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil
import subprocess
import sys

from manager_common import (
    BEGIN_MARKER,
    END_MARKER,
    MANAGER_VERSION,
    ManagerConfig,
    ManagerError,
    default_agents_file,
    default_config_file,
    install_managed_instructions,
    load_config,
    validate_roots,
    write_config,
)


OFFICIAL_REMOTE = "https://github.com/Nuowl/codex-project-template.git"
LEGACY_TEMPLATE_FILES = (
    "AGENTS_REQ.md",
    "OPERATING_GUIDE.md",
    "PATH.md",
    "PROJECT_CREATION_RUNBOOK.md",
    "PROJECT_FILE_SKELETONS.md",
    "PROJECT_TEMPLATE_PROMPT.md",
    "README.md",
    "install_agents.py",
    "manager_common.py",
    "migrate_projects.py",
    "setup.py",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install or update Codex project manager configuration."
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        help="User project workspace (default: sibling codex_projects directory)",
    )
    parser.add_argument("--config-file", type=Path, default=default_config_file())
    parser.add_argument("--agents-file", type=Path, default=default_agents_file())
    parser.add_argument(
        "--adopt-legacy",
        action="store_true",
        help="Archive known legacy template files from an existing workspace",
    )
    parser.add_argument(
        "--check", action="store_true", help="Validate and report without changes"
    )
    parser.add_argument(
        "--no-update",
        action="store_true",
        help="Skip the Git update and configure the current manager files",
    )
    parser.add_argument("--post-update", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args()


def _git(manager_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(manager_root), *args],
        check=False,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise ManagerError(f"Git command failed ({' '.join(args)}): {message}")
    return result.stdout.strip()


def _normalized_remote(url: str) -> str:
    normalized = url.strip().rstrip("/")
    if normalized.endswith(".git"):
        normalized = normalized[:-4]
    if normalized.startswith("git@github.com:"):
        normalized = "https://github.com/" + normalized.removeprefix("git@github.com:")
    return normalized.lower()


def update_manager(manager_root: Path, argv: list[str]) -> bool:
    if not (manager_root / ".git").is_dir():
        print("Git update skipped: manager directory is not a Git checkout")
        return False

    dirty = _git(manager_root, "status", "--porcelain", "--untracked-files=no")
    if dirty:
        raise ManagerError("Tracked manager files have uncommitted changes")

    remote = _git(manager_root, "remote", "get-url", "origin")
    if _normalized_remote(remote) != _normalized_remote(OFFICIAL_REMOTE):
        raise ManagerError(f"Unexpected Git origin: {remote}")

    branch = _git(manager_root, "branch", "--show-current")
    if not branch:
        raise ManagerError("Manager Git checkout is in detached HEAD state")

    before = _git(manager_root, "rev-parse", "HEAD")
    _git(manager_root, "fetch", "--quiet", "origin", branch)
    fetched = _git(manager_root, "rev-parse", "FETCH_HEAD")
    if before == fetched:
        print(f"Manager already current: {before[:12]}")
        return False

    ancestor = subprocess.run(
        [
            "git",
            "-C",
            str(manager_root),
            "merge-base",
            "--is-ancestor",
            before,
            fetched,
        ],
        check=False,
    )
    if ancestor.returncode != 0:
        raise ManagerError("Remote update is not a fast-forward")

    _git(manager_root, "merge", "--ff-only", "FETCH_HEAD")
    print(f"Manager updated: {before[:12]} -> {fetched[:12]}")

    if "--post-update" not in argv:
        os.execv(
            sys.executable,
            [sys.executable, str(manager_root / "setup.py"), *argv, "--post-update"],
        )
    return True


def legacy_files(workspace: Path) -> list[Path]:
    return [
        workspace / name
        for name in LEGACY_TEMPLATE_FILES
        if (workspace / name).is_file()
    ]


def adopt_legacy_workspace(workspace: Path) -> Path:
    candidates = legacy_files(workspace)
    if not candidates:
        raise ManagerError(f"No known legacy template files found in {workspace}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = workspace.parent / f"{workspace.name}_legacy_template_backup_{stamp}"
    if backup.exists():
        raise ManagerError(f"Legacy backup path already exists: {backup}")

    moved: list[tuple[Path, Path]] = []
    try:
        backup.mkdir(parents=False)
        for source in candidates:
            destination = backup / source.name
            shutil.move(str(source), str(destination))
            moved.append((source, destination))
    except Exception as exc:
        for source, destination in reversed(moved):
            if destination.exists() and not source.exists():
                shutil.move(str(destination), str(source))
        if backup.exists() and not any(backup.iterdir()):
            backup.rmdir()
        raise ManagerError(
            f"Legacy adoption failed and was rolled back: {exc}"
        ) from exc
    return backup


def _configured_paths(
    manager_root: Path, config_file: Path, workspace_arg: Path | None
) -> tuple[Path, Path, bool]:
    config_exists = config_file.expanduser().exists()
    if config_exists:
        config = load_config(config_file)
        if config.manager_root != manager_root.resolve():
            raise ManagerError(
                "Configured manager root differs from this setup.py location: "
                f"{config.manager_root}"
            )
        if (
            workspace_arg is not None
            and workspace_arg.expanduser().resolve() != config.workspace_root
        ):
            raise ManagerError(
                f"--workspace conflicts with configured workspace: {config.workspace_root}"
            )
        return config.manager_root, config.workspace_root, True

    workspace = workspace_arg or (manager_root.parent / "codex_projects")
    manager, workspace = validate_roots(manager_root, workspace)
    return manager, workspace, False


def _instruction_state(agents_file: Path) -> str:
    target = agents_file.expanduser()
    if not target.exists():
        return "not installed"
    try:
        text = target.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return f"unreadable ({exc})"
    begins = text.count(BEGIN_MARKER)
    ends = text.count(END_MARKER)
    return (
        "installed"
        if begins == 1 and ends == 1
        else f"invalid markers ({begins}/{ends})"
    )


def main() -> int:
    args = parse_args()
    manager_root = Path(__file__).resolve().parent
    config_file = args.config_file.expanduser().resolve()
    agents_file = args.agents_file.expanduser().resolve()

    try:
        manager, workspace, configured = _configured_paths(
            manager_root, config_file, args.workspace
        )

        if args.check:
            print(f"Manager: {manager}")
            print(f"Workspace: {workspace}")
            print(f"Configuration: {'installed' if configured else 'not installed'}")
            print(f"Instructions: {_instruction_state(agents_file)}")
            print(
                f"Legacy template files: {len(legacy_files(workspace)) if workspace.exists() else 0}"
            )
            return 0

        if configured and not args.no_update and not args.post_update:
            update_manager(manager, sys.argv[1:])

        if not configured and legacy_files(workspace) and not args.adopt_legacy:
            raise ManagerError(
                "Existing legacy template files were found in the workspace. "
                "Run setup.py again with --adopt-legacy."
            )

        if args.adopt_legacy:
            if not workspace.is_dir():
                raise ManagerError(f"Legacy workspace not found: {workspace}")
            backup = adopt_legacy_workspace(workspace)
            print(f"Legacy template backup: {backup}")
        else:
            workspace.mkdir(parents=True, exist_ok=True)

        validate_roots(manager, workspace)
        config = ManagerConfig(manager, workspace, MANAGER_VERSION)
        config_existed = config_file.exists()
        config_backup = write_config(config_file, config)
        try:
            agents_backup = install_managed_instructions(
                manager, workspace, agents_file
            )
        except Exception:
            if config_backup and config_backup.exists():
                shutil.copy2(config_backup, config_file)
            elif not config_existed:
                config_file.unlink(missing_ok=True)
            raise

        print(f"Manager: {manager}")
        print(f"Workspace: {workspace}")
        print(f"Configuration updated: {config_file}")
        print(f"Instructions updated: {agents_file}")
        if config_backup:
            print(f"Configuration backup: {config_backup}")
        if agents_backup:
            print(f"Instructions backup: {agents_backup}")
        print("Project migration was not run. Use migrate_projects.py separately.")
        return 0
    except (ManagerError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
