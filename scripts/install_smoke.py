#!/usr/bin/env python3
"""Verify a project-local copy installation with the documented Skills CLI."""

import hashlib
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix="skills-install-") as temporary:
        target = Path(temporary)
        subprocess.run(["git", "init", "-q", str(target)], check=True)
        subprocess.run(["npx", "--yes", "skills@1.5.25", "add", str(ROOT), "--agent", "codex", "--skill", "*", "--copy", "--yes"], cwd=target, check=True)
        skills = sorted((ROOT / "skills").iterdir())
        installed = target / ".agents/skills"
        if {p.name for p in installed.iterdir()} != {p.name for p in skills}:
            raise ValueError("installed skill inventory differs from source")
        for source in skills:
            for filename in ["SKILL.md", "LICENSE"]:
                expected = hashlib.sha256((source / filename).read_bytes()).digest()
                actual = hashlib.sha256((installed / source.name / filename).read_bytes()).digest()
                if expected != actual:
                    raise ValueError("installed file differs: " + source.name + "/" + filename)
        if not (target / "skills-lock.json").is_file():
            raise ValueError("installer did not record project provenance")
        print(f"Verified {len(skills)} installed skills and licenses without changing user-level settings")


if __name__ == "__main__":
    main()
