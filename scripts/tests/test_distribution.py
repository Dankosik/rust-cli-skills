import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile

SOURCE = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("distribution", SOURCE / "scripts/distribution.py")
distribution = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(distribution)


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / SOURCE.name
        shutil.copytree(SOURCE, self.root, ignore=shutil.ignore_patterns(".git", ".codegraph", "dist", ".venv", "__pycache__"))

    def check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return distribution.check(self.root)

    def test_manifests_and_skills_are_valid(self):
        self.assertEqual(self.check()["name"], SOURCE.name)

    def test_stale_native_version_is_rejected(self):
        path = self.root / ".claude-plugin/plugin.json"
        data = json.loads(path.read_text())
        data["version"] = "0.0.1"
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "metadata drift"):
            self.check()

    def test_standalone_license_is_required(self):
        skill = next((self.root / "skills").iterdir())
        (skill / "LICENSE").write_text("incomplete notice")
        with self.assertRaisesRegex(ValueError, "license differs"):
            self.check()

    def test_asset_symlink_is_rejected(self):
        link = self.root / "assets/external"
        link.symlink_to(self.root / "LICENSE")
        with self.assertRaisesRegex(ValueError, "symlinks"):
            self.check()

    def test_archive_is_reproducible_and_excludes_authoring_tools(self):
        commands = [["git", "init", "-q"], ["git", "add", "."], ["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"]]
        for command in commands:
            subprocess.run(command, cwd=self.root, check=True, capture_output=True)
        first, second = self.root / "dist/first", self.root / "dist/second"
        with contextlib.redirect_stdout(io.StringIO()):
            distribution.build(self.root, first)
            distribution.build(self.root, second)
        a = next(first.glob("*.zip"))
        b = next(second.glob("*.zip"))
        self.assertEqual(a.read_bytes(), b.read_bytes())
        with zipfile.ZipFile(a) as archive:
            names = archive.namelist()
            self.assertFalse(any("/scripts/" in name or "/.github/" in name for name in names))
            self.assertTrue(any(name.endswith("/.codex-plugin/plugin.json") for name in names))
            self.assertTrue(any(name.endswith("/.claude-plugin/plugin.json") for name in names))
            for skill in (self.root / "skills").iterdir():
                self.assertIn(SOURCE.name + "/skills/" + skill.name + "/LICENSE", names)


if __name__ == "__main__":
    unittest.main()
