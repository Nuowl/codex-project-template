from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from migrate_projects import apply_plan, inspect_project
from setup import _is_git_checkout, adopt_legacy_workspace


MANAGER_ROOT = Path(__file__).resolve().parents[1]


class SetupAndMigrationTests(unittest.TestCase):
    def run_command(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", *args],
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def project_snapshot(self, project: Path) -> dict[str, bytes]:
        return {
            str(path.relative_to(project)): path.read_bytes()
            for path in project.rglob("*")
            if path.is_file()
        }

    def test_setup_cli_installs_separate_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "workspace with spaces"
            config = root / "codex-projects.json"
            agents = root / "AGENTS.md"
            agents.write_text("# 개인 지침\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(MANAGER_ROOT / "setup.py"),
                    "--no-update",
                    "--workspace",
                    str(workspace),
                    "--config-file",
                    str(config),
                    "--agents-file",
                    str(agents),
                ],
                text=True,
                encoding="utf-8",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(config.read_text(encoding="utf-8"))
            self.assertEqual(data["workspace_root"], str(workspace.resolve()))
            installed = agents.read_text(encoding="utf-8")
            self.assertIn("# 개인 지침", installed)
            self.assertIn(str(MANAGER_ROOT), installed)
            self.assertIn(str(workspace.resolve()), installed)
            self.assertNotIn("<CODEX_PROJECT", installed)

    def test_separate_git_dir_is_recognized_as_git_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            worktree = root / "worktree"
            git_dir = root / "gitdir.git"

            subprocess.run(["git", "init", source], check=True, stdout=subprocess.PIPE)
            (source / "README.md").write_text("source\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(source),
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.invalid",
                    "commit",
                    "-m",
                    "init",
                ],
                check=True,
                stdout=subprocess.PIPE,
            )
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--no-checkout",
                    "--separate-git-dir",
                    str(git_dir),
                    str(source),
                    str(worktree),
                ],
                check=True,
                stdout=subprocess.PIPE,
            )

            self.assertTrue((worktree / ".git").is_file())
            self.assertTrue(_is_git_checkout(worktree))
    def test_setup_requires_adoption_for_mixed_legacy_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "codex_projects"
            workspace.mkdir()
            (workspace / "README.md").write_text("legacy template\n", encoding="utf-8")
            config = root / "config.json"
            agents = root / "AGENTS.md"

            result = self.run_command(
                str(MANAGER_ROOT / "setup.py"),
                "--no-update",
                "--workspace",
                str(workspace),
                "--config-file",
                str(config),
                "--agents-file",
                str(agents),
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("--adopt-legacy", result.stderr)
            self.assertFalse(config.exists())
            self.assertFalse(agents.exists())

    def test_legacy_adoption_removes_only_known_root_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "codex_projects"
            project = workspace / "Existing_Project"
            project.mkdir(parents=True)
            (project / "NOTES.md").write_text("project data\n", encoding="utf-8")
            (workspace / "README.md").write_text("legacy template\n", encoding="utf-8")
            (workspace / "AGENTS_REQ.md").write_text(
                "legacy instructions\n", encoding="utf-8"
            )
            (workspace / "LEGACY_MIGRATION.md").write_text(
                "legacy guide\n", encoding="utf-8"
            )
            (workspace / ".gitignore").write_text("legacy ignores\n", encoding="utf-8")
            (workspace / "tests").mkdir()
            (workspace / "tests" / "test_legacy.py").write_text(
                "legacy tests\n", encoding="utf-8"
            )
            (workspace / "user-root-note.txt").write_text("keep\n", encoding="utf-8")

            removed = adopt_legacy_workspace(workspace)

            self.assertEqual(removed, 5)
            self.assertFalse(
                list(root.glob(f"{workspace.name}_legacy_template_backup_*"))
            )
            self.assertFalse(
                list(root.glob(f"{workspace.name}_legacy_template_cleanup_*"))
            )
            self.assertTrue((project / "NOTES.md").is_file())
            self.assertTrue((workspace / "user-root-note.txt").is_file())
            self.assertFalse((workspace / "README.md").exists())
            self.assertFalse((workspace / "LEGACY_MIGRATION.md").exists())
            self.assertFalse((workspace / ".gitignore").exists())
            self.assertFalse((workspace / "tests").exists())

    def test_migration_preserves_existing_content_and_creates_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "Legacy_Project"
            status = project / "plans" / "STATUS.md"
            status.parent.mkdir(parents=True)
            original_notes = "# Existing notes\n\nDo not replace this content.\n"
            original_status = "# Status\n\n## Current State\n\n- Existing state\n"
            (project / "NOTES.md").write_text(original_notes, encoding="utf-8")
            status.write_text(original_status, encoding="utf-8")

            plan = inspect_project(project)
            self.assertEqual(plan.classification, "legacy")
            self.assertFalse((project / ".codex-project.json").exists())

            backup_root = root / "backups"
            backup_root.mkdir()
            apply_plan(plan, MANAGER_ROOT, backup_root)

            self.assertEqual(
                (project / "NOTES.md").read_text(encoding="utf-8"), original_notes
            )
            migrated_status = status.read_text(encoding="utf-8")
            self.assertIn("- Existing state", migrated_status)
            for heading in (
                "Last Updated",
                "Current State",
                "Last Completed",
                "Next Action",
                "Blocked By",
            ):
                self.assertIn(f"## {heading}", migrated_status)
            identity = json.loads(
                (project / ".codex-project.json").read_text(encoding="utf-8")
            )
            self.assertEqual(identity["schema_version"], 2)
            self.assertNotIn("version", identity)
            self.assertEqual(identity["manager_version"], "V4_260706")
            self.assertTrue((project / "plans" / "REQUIREMENTS.md").is_file())
            self.assertEqual(
                (backup_root / "Legacy_Project" / "plans" / "STATUS.md").read_text(
                    encoding="utf-8"
                ),
                original_status,
            )

    def test_notes_only_project_is_migratable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "Notes_Only_Project"
            project.mkdir()
            original_notes = "# Existing notes\n\nDo not replace this content.\n"
            (project / "NOTES.md").write_text(original_notes, encoding="utf-8")

            plan = inspect_project(project)
            self.assertEqual(plan.classification, "legacy")
            self.assertIn("create file plans/STATUS.md", plan.actions)

            backup_root = root / "backups"
            backup_root.mkdir()
            apply_plan(plan, MANAGER_ROOT, backup_root)

            self.assertEqual(
                (project / "NOTES.md").read_text(encoding="utf-8"), original_notes
            )
            self.assertTrue((project / "plans" / "STATUS.md").is_file())
            self.assertTrue((project / ".codex-project.json").is_file())

    def test_conflicting_identity_is_not_migratable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "Actual_Name"
            project.mkdir()
            (project / ".codex-project.json").write_text(
                json.dumps(
                    {
                        "schema": "codex_projects",
                        "schema_version": 1,
                        "project_name": "Example",
                        "project_folder": "Wrong_Name",
                        "created_at": "2026-06-22",
                    }
                ),
                encoding="utf-8",
            )
            plan = inspect_project(project)
            self.assertEqual(plan.classification, "conflicting")

    def test_legacy_version_key_is_renamed_to_schema_version(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "Legacy_Key_Project"
            project.mkdir()
            (project / ".codex-project.json").write_text(
                json.dumps(
                    {
                        "schema": "codex_projects",
                        "version": 2,
                        "project_name": "Legacy Key Project",
                        "project_folder": "Legacy_Key_Project",
                        "created_at": "2026-07-06",
                        "manager_version": "V4_260622",
                    }
                ),
                encoding="utf-8",
            )

            plan = inspect_project(project)
            self.assertEqual(plan.classification, "legacy")
            self.assertIn("set schema_version 2", plan.actions)

            backup_root = root / "backups"
            backup_root.mkdir()
            apply_plan(plan, MANAGER_ROOT, backup_root)

            identity = json.loads(
                (project / ".codex-project.json").read_text(encoding="utf-8")
            )
            self.assertNotIn("version", identity)
            self.assertEqual(identity["schema_version"], 2)
            self.assertEqual(identity["manager_version"], "V4_260706")

    def test_project_symlink_is_conflicting(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "target"
            target.mkdir()
            project = root / "linked-project"
            try:
                project.symlink_to(target, target_is_directory=True)
            except OSError as exc:
                if getattr(exc, "winerror", None) == 1314:
                    self.skipTest("Windows symlink privilege is unavailable")
                raise

            plan = inspect_project(project)

            self.assertEqual(plan.classification, "conflicting")
            self.assertIn("symlink", (plan.error or "").lower())

    def test_full_legacy_adoption_and_migration_cli(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "한글 workspace"
            project = workspace / "Legacy Project"
            status = project / "plans" / "STATUS.md"
            status.parent.mkdir(parents=True)
            (project / "NOTES.md").write_text("# 기존 프로젝트\n", encoding="utf-8")
            status.write_text(
                "# Status\n\n## Current State\n\n- 기존 상태\n", encoding="utf-8"
            )
            (workspace / "README.md").write_text("legacy template\n", encoding="utf-8")
            config = root / "config.json"
            agents = root / "AGENTS.md"

            before_adoption = self.project_snapshot(project)
            setup_result = self.run_command(
                str(MANAGER_ROOT / "setup.py"),
                "--no-update",
                "--workspace",
                str(workspace),
                "--adopt-legacy",
                "--config-file",
                str(config),
                "--agents-file",
                str(agents),
            )
            self.assertEqual(setup_result.returncode, 0, setup_result.stderr)
            self.assertEqual(self.project_snapshot(project), before_adoption)
            self.assertIn("Legacy template files removed: 1", setup_result.stdout)
            self.assertFalse(
                list(root.glob(f"{workspace.name}_legacy_template_backup_*"))
            )
            self.assertFalse(
                list(root.glob(f"{workspace.name}_legacy_template_cleanup_*"))
            )

            dry_run = self.run_command(
                str(MANAGER_ROOT / "migrate_projects.py"),
                "--all",
                "--config-file",
                str(config),
            )
            self.assertEqual(dry_run.returncode, 0, dry_run.stderr)
            self.assertIn("Preview: 1 project(s)", dry_run.stdout)
            self.assertIn("Legacy Project: needs update", dry_run.stdout)
            self.assertNotIn("create file", dry_run.stdout)
            self.assertEqual(self.project_snapshot(project), before_adoption)

            verbose_dry_run = self.run_command(
                str(MANAGER_ROOT / "migrate_projects.py"),
                "--all",
                "--verbose",
                "--config-file",
                str(config),
            )
            self.assertEqual(verbose_dry_run.returncode, 0, verbose_dry_run.stderr)
            self.assertIn("create file", verbose_dry_run.stdout)

            apply = self.run_command(
                str(MANAGER_ROOT / "migrate_projects.py"),
                "--all",
                "--apply",
                "--config-file",
                str(config),
            )
            self.assertEqual(apply.returncode, 0, apply.stderr)
            self.assertTrue((project / ".codex-project.json").is_file())
            self.assertTrue((workspace / ".codex-project-backups").exists())
            self.assertFalse((workspace / ".codex-migration-reports").exists())
            self.assertFalse(
                list(root.glob(f"{workspace.name}_legacy_template_backup_*"))
            )
            self.assertFalse(
                list(root.glob(f"{workspace.name}_legacy_template_cleanup_*"))
            )
            after_migration = self.project_snapshot(project)

            repeat_setup = self.run_command(
                str(MANAGER_ROOT / "setup.py"),
                "--no-update",
                "--config-file",
                str(config),
                "--agents-file",
                str(agents),
            )
            self.assertEqual(repeat_setup.returncode, 0, repeat_setup.stderr)
            self.assertEqual(self.project_snapshot(project), after_migration)

            current_check = self.run_command(
                str(MANAGER_ROOT / "migrate_projects.py"),
                "--all",
                "--config-file",
                str(config),
            )
            self.assertEqual(current_check.returncode, 0, current_check.stderr)
            self.assertIn("Legacy Project: up to date", current_check.stdout)


if __name__ == "__main__":
    unittest.main()
