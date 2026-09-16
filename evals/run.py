#!/usr/bin/env python3
"""Prepare isolated tasks and grade artifacts; never invokes a model."""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time
import tomllib

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
FIXTURES = {"R01", "R05", "R06"}
MARKERS = {"R05": b"R05:9 checks complete\n", "R06": b"R06:5 checks complete\n"}
MAX_SOURCE_BYTES = 1024 * 1024
MAX_LOG_BYTES = 256 * 1024


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def catalogue() -> dict:
    data = json.loads((EVALS / "cases.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("unsupported catalogue schema")
    cases = {}
    for case in data["cases"]:
        name = case["id"]
        if name in cases or case["mode"] not in {"artifact", "manual"}:
            raise ValueError("duplicate case or invalid mode: " + name)
        if (case["mode"] == "artifact") != (case["fixture"] in FIXTURES):
            raise ValueError("invalid fixture mapping: " + name)
        if not case["prompt"] or not case["accept"] or not case["reject"]:
            raise ValueError("missing prompt or evaluator rubric: " + name)
        cases[name] = case
    return cases


def selected(case_id: str) -> dict:
    try:
        return catalogue()[case_id]
    except KeyError as error:
        raise ValueError("unknown case: " + case_id) from error


def regular_files(folder: Path) -> dict[str, bytes]:
    """Read a small, quiescent source tree; reject symlinks and special files."""
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("expected a regular source directory")
    files = {}
    total = 0
    for path in sorted(folder.rglob("*")):
        if path.is_symlink():
            raise ValueError("symlink in source: " + str(path))
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError("non-regular source: " + str(path))
        if len(files) >= 64 or path.stat().st_size + total > MAX_SOURCE_BYTES:
            raise ValueError("source exceeds fixture budget")
        # The host must stop concurrent writes before grading; this is not a sandbox.
        with path.open("rb") as stream:
            content = stream.read(MAX_SOURCE_BYTES - total + 1)
        total += len(content)
        if total > MAX_SOURCE_BYTES:
            raise ValueError("source exceeds fixture budget")
        files[path.relative_to(folder).as_posix()] = content
    return files


def content_hash(files: dict[str, bytes]) -> str:
    entries = {path: sha256(content) for path, content in sorted(files.items())}
    return sha256(json.dumps(entries, sort_keys=True).encode("utf-8"))


def prepare(case_id: str, destination: Path) -> dict:
    case = selected(case_id)
    if case["mode"] != "artifact":
        raise ValueError("manual control: present its prompt without an invented fixture")
    destination = destination.absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError("destination must not exist")
    if destination.resolve().is_relative_to(ROOT):
        raise ValueError("prepare outside the author checkout to avoid context contamination")
    fixture = EVALS / "fixtures" / case["fixture"]
    files = regular_files(fixture)
    destination.mkdir(parents=True)
    for relative, content in files.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    return {"case": case_id, "status": "prepared", "workspace": str(destination),
            "fixture_sha256": content_hash(files), "prompt": case["prompt"]}


def run_bounded(command: list[str], cwd: Path, *, timeout: float,
                env: dict | None = None, limit: int = MAX_LOG_BYTES) -> dict:
    """Bound waiting and captured bytes; terminate the POSIX process group."""
    if not math.isfinite(timeout) or timeout <= 0 or limit <= 0:
        raise ValueError("timeout and output limit must be positive and finite")
    if os.name != "posix":
        return {"state": "blocked", "reason": "execution currently requires POSIX process groups"}
    started = time.monotonic()
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        try:
            process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                       stdout=stdout, stderr=stderr, start_new_session=True)
        except OSError as error:
            return {"state": "blocked", "reason": str(error)}
        state = "exited"
        try:
            while True:
                if os.fstat(stdout.fileno()).st_size + os.fstat(stderr.fileno()).st_size > limit:
                    state = "output_limit"
                    break
                if process.poll() is not None:
                    break
                if time.monotonic() - started >= timeout:
                    state = "timeout"
                    break
                time.sleep(0.01)
        finally:
            # Clean descendants even if the direct child has already returned.
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()
        if os.fstat(stdout.fileno()).st_size + os.fstat(stderr.fileno()).st_size > limit:
            state = "output_limit"
        stdout.seek(0)
        stderr.seek(0)
        out = stdout.read(limit)
        err = stderr.read(max(0, limit - len(out)))
    return {"state": state, "returncode": process.returncode, "stdout": out,
            "stderr": err, "seconds": time.monotonic() - started}


def observation(result: dict, command: list[str]) -> dict:
    """Preserve raw byte evidence without depending on lossy display strings."""
    return {"command": command, **{key: value for key, value in result.items()
                                   if key not in {"stdout", "stderr"}},
            "stdout_hex": result.get("stdout", b"").hex(),
            "stderr_hex": result.get("stderr", b"").hex()}


def stage_result(result: dict) -> str:
    if result["state"] == "blocked":
        return "blocked"
    if result["state"] != "exited":
        return "incomplete"
    return "pass" if result["returncode"] == 0 else "fail"


def grade(case_id: str, workspace: Path, *, timeout: float = 30.0) -> dict:
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be positive and finite")
    case = selected(case_id)
    report = {"case": case_id, "artifact_result": "not_run", "stage": "setup",
              "behavior_result": "not_assessed", "observations": [],
              "grader_sha256": sha256(Path(__file__).read_bytes())}
    if case["mode"] != "artifact":
        report.update(artifact_result="not_applicable", reason="manual prompt/trace control")
        return report
    fixture_id = case["fixture"]
    fixture = EVALS / "fixtures" / fixture_id
    baseline = regular_files(fixture)
    oracle = EVALS / "oracles" / (fixture_id + (".json" if fixture_id == "R01" else ".rs"))
    report.update(fixture_sha256=content_hash(baseline), oracle_sha256=sha256(oracle.read_bytes()))
    try:
        if workspace.is_symlink() or not workspace.is_dir():
            raise ValueError("workspace must be a regular directory")
        for relative in ["Cargo.toml", "Cargo.lock"]:
            path = workspace / relative
            if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_SOURCE_BYTES:
                raise ValueError("invalid manifest/lockfile: " + relative)
            if tomllib.loads(path.read_text(encoding="utf-8")) != tomllib.loads(baseline[relative].decode("utf-8")):
                raise ValueError("fixture manifest/lockfile contract changed: " + relative)
        for relative in ["build.rs", ".cargo"]:
            if (workspace / relative).exists() or (workspace / relative).is_symlink():
                raise ValueError("unrequested build configuration: " + relative)
        source = regular_files(workspace / "src")
        if "lib.rs" not in source or "main.rs" not in source:
            raise ValueError("fixture source entry point missing")
    except (OSError, ValueError) as error:
        report.update(artifact_result="fail", stage="scope", reason=str(error))
        return report
    report.update(source_sha256=content_hash(source), graded_files=sorted("src/" + p for p in source))
    cargo = shutil.which("cargo")
    if cargo is None:
        report.update(artifact_result="blocked", reason="Cargo is unavailable; no Rust checks ran")
        return report
    with tempfile.TemporaryDirectory(prefix="rust-skill-grade-") as temporary:
        stage = Path(temporary)
        for relative, content in source.items():
            target = stage / "src" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        manifest = baseline["Cargo.toml"]
        if fixture_id != "R01":
            manifest += b'\n[[bin]]\nname = "evaluation-oracle"\npath = "evaluation-oracle.rs"\n'
            (stage / "evaluation-oracle.rs").write_bytes(oracle.read_bytes())
        (stage / "Cargo.toml").write_bytes(manifest)
        (stage / "Cargo.lock").write_bytes(baseline["Cargo.lock"])
        # Deliberately do not load candidate build scripts, Cargo config or tests.
        env = {key: os.environ[key] for key in
               ["PATH", "HOME", "RUSTUP_HOME", "RUSTUP_TOOLCHAIN", "TMPDIR"] if key in os.environ}
        env.update(CARGO_HOME=str(stage / "cargo-home"), CARGO_TARGET_DIR=str(stage / "target"),
                   CARGO_TERM_COLOR="never", CARGO_INCREMENTAL="0", RUST_BACKTRACE="0")
        command = [cargo, "build", "--locked", "--offline", "--bins", "--jobs", "1"]
        build = run_bounded(command, stage, timeout=timeout, env=env)
        report["observations"].append(observation(build, command))
        status = stage_result(build)
        if status != "pass":
            report.update(artifact_result=status, stage="build")
            return report
        if fixture_id == "R01":
            checks = json.loads(oracle.read_text(encoding="utf-8"))
            if not checks:
                report.update(artifact_result="incomplete", stage="oracle", reason="empty oracle")
                return report
            for index, check in enumerate(checks, 1):
                command = [str(stage / "target/debug/fixture-cli"), *check["args"]]
                result = run_bounded(command, stage, timeout=min(timeout, 5.0), env=env)
                report["observations"].append(observation(result, command))
                status = stage_result(result)
                if result["state"] != "exited":
                    report.update(artifact_result=status, stage="oracle", check=index)
                    return report
                expected = (check["status"], check["stdout"].encode(), check["stderr"].encode())
                actual = (result["returncode"], result["stdout"], result["stderr"])
                if actual != expected:
                    report.update(artifact_result="fail", stage="oracle", check=index,
                                  expected={"status": expected[0], "stdout_hex": expected[1].hex(),
                                            "stderr_hex": expected[2].hex()})
                    return report
        else:
            command = [str(stage / "target/debug/evaluation-oracle")]
            result = run_bounded(command, stage, timeout=min(timeout, 5.0), env=env)
            report["observations"].append(observation(result, command))
            status = stage_result(result)
            if status != "pass":
                report.update(artifact_result=status, stage="oracle")
                return report
            if result["stdout"] != MARKERS[fixture_id]:
                report.update(artifact_result="incomplete", stage="oracle",
                              reason="oracle exited without its completion record")
                return report
    report.update(artifact_result="pass", stage="oracle")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="print evaluator catalogue; do not give its rubric to the trial agent")
    prepare_parser = sub.add_parser("prepare")
    prepare_parser.add_argument("case")
    prepare_parser.add_argument("destination", type=Path)
    grade_parser = sub.add_parser("grade")
    grade_parser.add_argument("case")
    grade_parser.add_argument("workspace", type=Path)
    grade_parser.add_argument("--timeout", type=float, default=30.0, help="seconds per build; each probe is capped at 5 seconds")
    args = parser.parse_args()
    try:
        if args.command == "list":
            result = catalogue()
        elif args.command == "prepare":
            result = prepare(args.case, args.destination)
        else:
            result = grade(args.case, args.workspace, timeout=args.timeout)
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + "\n")
    print(json.dumps(result, indent=2))
    if args.command != "grade":
        return 0
    return {"pass": 0, "fail": 1}.get(result["artifact_result"], 2)


if __name__ == "__main__":
    raise SystemExit(main())
