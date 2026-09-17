"""Fast harness checks; optional std-only Rust oracle sensitivity checks."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("skill_evaluation", ROOT / "evals/run.py")
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)


def exited(code=0, stdout=b"", stderr=b""):
    return {"state": "exited", "returncode": code, "stdout": stdout,
            "stderr": stderr, "seconds": 0.0}


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skill-eval-test-")
        self.addCleanup(self.temporary.cleanup)
        self.parent = Path(self.temporary.name)
        self.workspace = self.parent / "trial"

    def test_catalogue_has_explicit_implicit_contextual_and_negative_cases(self):
        cases = evaluation.catalogue()
        self.assertEqual(len(cases), 12)
        self.assertEqual(sum(case["mode"] == "manual" for case in cases.values()), 8)
        self.assertEqual({case["trigger"] for case in cases.values()},
                         {"implicit", "explicit", "contextual", "negative"})
        self.assertEqual(cases["R05"]["fixture"], cases["E05"]["fixture"])

    def test_prepare_withholds_oracle_rubric_repair_and_author_instructions(self):
        prepared = evaluation.prepare("R05", self.workspace)
        names = set(evaluation.regular_files(self.workspace))
        self.assertEqual(names, {"Cargo.toml", "Cargo.lock", "README.md", ".gitignore",
                                "src/lib.rs", "src/main.rs"})
        self.assertNotIn("accept", prepared)
        self.assertNotIn("areas", prepared)
        self.assertEqual(prepared["fixture_sha256"],
                         evaluation.content_hash(evaluation.regular_files(self.workspace)))

    def test_prepare_refuses_existing_destination(self):
        self.workspace.mkdir()
        marker = self.workspace / "preserve"
        marker.write_text("user data", encoding="utf-8")
        with self.assertRaises(ValueError):
            evaluation.prepare("R01", self.workspace)
        self.assertEqual(marker.read_text(), "user data")

    def test_prepare_refuses_author_checkout(self):
        with self.assertRaises(ValueError):
            evaluation.prepare("R01", ROOT / "evals/should-not-exist")
        self.assertFalse((ROOT / "evals/should-not-exist").exists())

    def test_manual_case_does_not_invent_artifact_result(self):
        report = evaluation.grade("N02", self.workspace)
        self.assertEqual(report["artifact_result"], "not_applicable")
        self.assertEqual(report["behavior_result"], "not_assessed")
        with self.assertRaises(ValueError):
            evaluation.prepare("N02", self.workspace)

    def test_missing_cargo_is_blocked_not_pass(self):
        evaluation.prepare("R01", self.workspace)
        with patch.object(evaluation.shutil, "which", return_value=None):
            report = evaluation.grade("R01", self.workspace)
        self.assertEqual(report["artifact_result"], "blocked")
        self.assertEqual(report["observations"], [])

    def test_changed_manifest_is_not_executed(self):
        evaluation.prepare("R01", self.workspace)
        with (self.workspace / "Cargo.toml").open("a") as output:
            output.write('\n[dependencies]\nunrequested = "1"\n')
        with patch.object(evaluation, "run_bounded") as run:
            report = evaluation.grade("R01", self.workspace)
        run.assert_not_called()
        self.assertEqual((report["artifact_result"], report["stage"]), ("fail", "scope"))

    def test_manifest_comments_do_not_become_false_scope_failures(self):
        evaluation.prepare("R01", self.workspace)
        with (self.workspace / "Cargo.toml").open("a") as output:
            output.write("\n# harmless formatting change\n")
        with patch.object(evaluation.shutil, "which", return_value=None):
            report = evaluation.grade("R01", self.workspace)
        self.assertEqual(report["artifact_result"], "blocked")

    def test_oversized_source_is_rejected_before_execution(self):
        evaluation.prepare("R01", self.workspace)
        (self.workspace / "src/oversized.rs").write_bytes(b"x" * (evaluation.MAX_SOURCE_BYTES + 1))
        with patch.object(evaluation, "run_bounded") as run:
            report = evaluation.grade("R01", self.workspace)
        run.assert_not_called()
        self.assertEqual((report["artifact_result"], report["stage"]), ("fail", "scope"))

    @unittest.skipUnless(os.name == "posix", "POSIX symlink fixture")
    def test_source_symlink_is_not_followed(self):
        evaluation.prepare("R01", self.workspace)
        secret = self.parent / "secret"
        secret.write_text("not task input", encoding="utf-8")
        (self.workspace / "src/escape.rs").symlink_to(secret)
        report = evaluation.grade("R01", self.workspace)
        self.assertEqual((report["artifact_result"], report["stage"]), ("fail", "scope"))

    def test_missing_oracle_completion_is_incomplete(self):
        evaluation.prepare("R05", self.workspace)
        with patch.object(evaluation.shutil, "which", return_value="cargo"), \
             patch.object(evaluation, "run_bounded", side_effect=[exited(), exited()]):
            report = evaluation.grade("R05", self.workspace)
        self.assertEqual((report["artifact_result"], report["stage"]), ("incomplete", "oracle"))

    def test_compile_failure_is_not_a_behavioral_red_test(self):
        evaluation.prepare("R05", self.workspace)
        with patch.object(evaluation.shutil, "which", return_value="cargo"), \
             patch.object(evaluation, "run_bounded", return_value=exited(101, stderr=b"compile error")):
            report = evaluation.grade("R05", self.workspace)
        self.assertEqual((report["artifact_result"], report["stage"]), ("fail", "build"))

    def test_artifact_pass_is_not_a_behavioral_verdict(self):
        evaluation.prepare("R06", self.workspace)
        with patch.object(evaluation.shutil, "which", return_value="cargo"), \
             patch.object(evaluation, "run_bounded", side_effect=[exited(), exited(stdout=evaluation.MARKERS["R06"])]):
            report = evaluation.grade("R06", self.workspace)
        self.assertEqual(report["artifact_result"], "pass")
        self.assertEqual(report["behavior_result"], "not_assessed")
        json.dumps(report)  # Raw bytes have a lossless serializable representation.

    def test_timeout_validation(self):
        for value in [0, -1, float("inf"), float("nan")]:
            with self.subTest(timeout=value), self.assertRaises(ValueError):
                evaluation.grade("R05", self.workspace, timeout=value)

    @unittest.skipUnless(os.name == "posix", "execution uses POSIX process groups")
    def test_capture_preserves_bytes_and_exit_status(self):
        result = evaluation.run_bounded(
            [sys.executable, "-c", "import os; os.write(1,b'\\xff\\x00'); os.write(2,b'err'); raise SystemExit(3)"],
            self.parent, timeout=3)
        self.assertEqual(result["state"], "exited")
        self.assertEqual((result["returncode"], result["stdout"], result["stderr"]), (3, b"\xff\0", b"err"))

    @unittest.skipUnless(os.name == "posix", "execution uses POSIX process groups")
    def test_timeout_terminates_child_and_is_incomplete(self):
        result = evaluation.run_bounded([sys.executable, "-c", "import time; time.sleep(60)"],
                                        self.parent, timeout=0.1)
        self.assertEqual(result["state"], "timeout")
        self.assertEqual(evaluation.stage_result(result), "incomplete")
        self.assertIsNotNone(result["returncode"])

    @unittest.skipUnless(os.name == "posix", "execution uses POSIX process groups")
    def test_excess_output_does_not_fill_memory_or_pass(self):
        result = evaluation.run_bounded(
            [sys.executable, "-c", "import os\nwhile True: os.write(1, b'x'*8192)"],
            self.parent, timeout=3, limit=16384)
        self.assertEqual(result["state"], "output_limit")
        self.assertLessEqual(len(result["stdout"]) + len(result["stderr"]), 16384)
        self.assertEqual(evaluation.stage_result(result), "incomplete")

    @unittest.skipUnless(shutil.which("cargo") and os.name == "posix", "Cargo/POSIX unavailable: Rust oracle checks not run")
    def test_rust_oracles_reject_known_defects_and_accept_known_repairs(self):
        for name in ["R01", "R05", "R06"]:
            with self.subTest(case=name):
                workspace = self.parent / name
                evaluation.prepare(name, workspace)
                before = evaluation.grade(name, workspace)
                self.assertEqual((before["artifact_result"], before["stage"]), ("fail", "oracle"), before)
                shutil.copyfile(ROOT / "evals/repairs" / (name + ".rs"), workspace / "src/lib.rs")
                after = evaluation.grade(name, workspace)
                self.assertEqual(after["artifact_result"], "pass", after)


if __name__ == "__main__":
    unittest.main()
