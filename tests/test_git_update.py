from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from manager_common import ManagerError
from setup import update_manager


def git(directory: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(directory), *args],
        check=True,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


class GitUpdateTests(unittest.TestCase):
    def make_repositories(self, root: Path) -> tuple[Path, Path, Path]:
        remote = root / "remote.git"
        seed = root / "seed"
        manager = root / "manager"
        subprocess.run(
            ["git", "init", "--bare", "--initial-branch=main", str(remote)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        seed.mkdir()
        git(seed, "init", "-b", "main")
        git(seed, "config", "user.email", "tests@example.com")
        git(seed, "config", "user.name", "Tests")
        (seed / "version.txt").write_text("one\n", encoding="utf-8")
        git(seed, "add", "version.txt")
        git(seed, "commit", "-m", "initial")
        git(seed, "remote", "add", "origin", str(remote))
        git(seed, "push", "-u", "origin", "main")
        subprocess.run(
            ["git", "clone", "--branch", "main", str(remote), str(manager)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return remote, seed, manager

    def test_fast_forward_update(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            remote, seed, manager = self.make_repositories(Path(temp))
            (seed / "version.txt").write_text("two\n", encoding="utf-8")
            git(seed, "add", "version.txt")
            git(seed, "commit", "-m", "update")
            git(seed, "push", "origin", "main")

            with patch("setup.OFFICIAL_REMOTE", str(remote)):
                changed = update_manager(manager, ["--post-update"])

            self.assertTrue(changed)
            self.assertEqual(
                (manager / "version.txt").read_text(encoding="utf-8"), "two\n"
            )

    def test_dirty_tracked_file_blocks_update(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            remote, _seed, manager = self.make_repositories(Path(temp))
            (manager / "version.txt").write_text("dirty\n", encoding="utf-8")

            with patch("setup.OFFICIAL_REMOTE", str(remote)):
                with self.assertRaises(ManagerError):
                    update_manager(manager, ["--post-update"])


if __name__ == "__main__":
    unittest.main()
