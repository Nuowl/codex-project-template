from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from manager_common import (
    BEGIN_MARKER,
    END_MARKER,
    ManagerConfig,
    ManagerError,
    install_managed_instructions,
    load_config,
    validate_roots,
    write_config,
)


REQUIRED_FILES = (
    "AGENTS_REQ.md",
    "PROJECT_CREATION_RUNBOOK.md",
    "PROJECT_FILE_SKELETONS.md",
    "setup.py",
    "migrate_projects.py",
    "manager_common.py",
)


class ManagerCommonTests(unittest.TestCase):
    def make_manager(self, root: Path) -> Path:
        manager = root / "manager"
        manager.mkdir()
        for name in REQUIRED_FILES:
            content = ""
            if name == "AGENTS_REQ.md":
                content = (
                    "Manager: <CODEX_PROJECT_MANAGER_ROOT>\n"
                    "Workspace: <CODEX_PROJECTS_WORKSPACE_ROOT>\n"
                    "한글 지침\n"
                )
            (manager / name).write_text(content, encoding="utf-8")
        return manager

    def test_roots_must_be_separate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manager = self.make_manager(root)
            with self.assertRaises(ManagerError):
                validate_roots(manager, manager / "projects")

    def test_config_round_trip_and_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manager = self.make_manager(root)
            workspace = root / "workspace"
            workspace.mkdir()
            config_file = root / "config.json"
            config = ManagerConfig(manager.resolve(), workspace.resolve())

            self.assertIsNone(write_config(config_file, config))
            self.assertEqual(load_config(config_file), config)
            backup = write_config(config_file, config)
            self.assertEqual(backup, root / "config.json.bak")
            self.assertEqual(
                json.loads(backup.read_text(encoding="utf-8"))["schema"],
                "codex_project_manager",
            )

    def test_managed_block_is_replaced_and_personal_text_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manager = self.make_manager(root)
            workspace = root / "workspace"
            workspace.mkdir()
            agents = root / "AGENTS.md"
            agents.write_text("# 개인 지침\n\n보존\n", encoding="utf-8")

            install_managed_instructions(manager, workspace, agents)
            install_managed_instructions(manager, workspace, agents)
            installed = agents.read_text(encoding="utf-8")

            self.assertEqual(installed.count(BEGIN_MARKER), 1)
            self.assertEqual(installed.count(END_MARKER), 1)
            self.assertIn("# 개인 지침", installed)
            self.assertIn("한글 지침", installed)
            self.assertIn(str(manager.resolve()), installed)
            self.assertIn(str(workspace.resolve()), installed)
            self.assertNotIn("<CODEX_PROJECT", installed)


if __name__ == "__main__":
    unittest.main()
