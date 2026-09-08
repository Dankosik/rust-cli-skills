import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("publish", Path(__file__).resolve().parents[1] / "publish_release.py")
publish = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publish)


class PublicationTests(unittest.TestCase):
    def test_identical_complete_release_needs_no_upload(self):
        release = {"assets": [{"name": "pack.zip", "digest": "sha256:abc"}]}
        self.assertEqual(publish.verify_assets(release, {"pack.zip": "abc"}, True), set())

    def test_draft_can_resume_only_missing_files(self):
        release = {"assets": [{"name": "pack.zip", "digest": "sha256:abc"}]}
        self.assertEqual(publish.verify_assets(release, {"pack.zip": "abc", "SHA256SUMS": "def"}, False), {"SHA256SUMS"})
        with self.assertRaisesRegex(ValueError, "missing"):
            publish.verify_assets(release, {"pack.zip": "abc", "SHA256SUMS": "def"}, True)

    def test_different_or_unknown_assets_are_preserved_by_refusal(self):
        with self.assertRaisesRegex(ValueError, "differs"):
            publish.verify_assets({"assets": [{"name": "pack.zip", "digest": "sha256:wrong"}]}, {"pack.zip": "abc"}, False)
        with self.assertRaisesRegex(ValueError, "unexpected"):
            publish.verify_assets({"assets": [{"name": "other.zip", "digest": "sha256:abc"}]}, {"pack.zip": "abc"}, False)


if __name__ == "__main__":
    unittest.main()
