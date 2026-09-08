#!/usr/bin/env python3
"""Synchronize metadata, validate a skill pack, or build its release archive."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

import jsonschema
from skills_ref import validate as validate_skill

ROOT = Path(__file__).resolve().parents[1]
EXTENSION = "io.github.dankosik.distribution"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def native_manifests(root):
    package = read_json(root / "plugin.json")
    ui = package["extensions"][EXTENSION]
    common = {key: package[key] for key in ("name", "version", "description", "author", "homepage", "repository", "license", "keywords")}
    codex = dict(common, skills="./skills/")
    codex["interface"] = {
        **{key: ui[key] for key in ("displayName", "shortDescription", "longDescription", "defaultPrompt", "brandColor")},
        "developerName": package["author"]["name"],
        "category": "Productivity",
        "capabilities": [],
        "websiteURL": package["homepage"],
        "privacyPolicyURL": package["repository"] + "/blob/main/PRIVACY.md",
        "termsOfServiceURL": package["repository"] + "/blob/main/LICENSE",
        "composerIcon": "./assets/logo.png",
        "logo": "./assets/logo.png",
    }
    return {".claude-plugin/plugin.json": common, ".codex-plugin/plugin.json": codex}


def synchronize(root):
    for relative, manifest in native_manifests(root).items():
        write_json(root / relative, manifest)
    license_bytes = (root / "LICENSE").read_bytes()
    for skill in (root / "skills").iterdir():
        if skill.is_dir() and (skill / "SKILL.md").is_file():
            (skill / "LICENSE").write_bytes(license_bytes)


def check(root):
    package = read_json(root / "plugin.json")
    jsonschema.Draft202012Validator(read_json(root / "scripts/plugin.schema.json")).validate(package)
    if not re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", package["version"]):
        raise ValueError("release version must be a stable MAJOR.MINOR.PATCH")
    for relative, expected in native_manifests(root).items():
        if read_json(root / relative) != expected:
            raise ValueError("derived metadata drift: run scripts/distribution.py sync (" + relative + ")")
    skills = sorted((root / "skills").iterdir())
    if len(skills) != package["extensions"][EXTENSION]["skillCount"]:
        raise ValueError("skillCount does not match the skill inventory")
    license_bytes = (root / "LICENSE").read_bytes()
    for skill in skills:
        if skill.is_symlink() or not skill.is_dir():
            raise ValueError("skill entries must be regular directories")
        if {p.name for p in skill.iterdir()} != {"SKILL.md", "LICENSE"}:
            raise ValueError("unexpected files in skill: " + skill.name)
        problems = validate_skill(skill)
        if problems:
            raise ValueError(skill.name + ": " + "; ".join(problems))
        if (skill / "LICENSE").read_bytes() != license_bytes:
            raise ValueError("individual skill license differs from package license")
    for path in list((root / "skills").rglob("*")) + list((root / "assets").rglob("*")):
        if path.is_symlink():
            raise ValueError("distributable paths must not be symlinks")
    for image in [root / "assets/logo.png", root / "assets/logo.svg"]:
        if not image.is_file():
            raise ValueError("missing logo asset: " + image.name)
    docs = [root / "README.md", root / "PRIVACY.md", root / "SUPPORT.md"] + list((root / "docs").glob("*.md"))
    for path in docs:
        for link in re.findall(r"\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
            if "://" not in link and not link.startswith(("#", "mailto:")):
                if link.startswith("/") or not (path.parent / link.split("#", 1)[0]).exists():
                    raise ValueError("broken local link in " + path.name + ": " + link)
    print(f"Validated {package['name']} {package['version']}: {len(skills)} skills and three manifests")
    return package


def build(root, destination):
    package = check(root)
    git = ["git", "-C", str(root)]
    if subprocess.check_output(git + ["status", "--porcelain"], text=True).strip():
        raise ValueError("release archives require a clean committed checkout")
    commit = subprocess.check_output(git + ["rev-parse", "HEAD"], text=True).strip()
    timestamp = int(subprocess.check_output(git + ["show", "-s", "--format=%ct", "HEAD"], text=True))
    date = datetime.fromtimestamp(max(timestamp, 315532800), timezone.utc).timetuple()[:6]
    files = [root / p for p in ["plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json", "README.md", "LICENSE", "PRIVACY.md", "SUPPORT.md", "CHANGELOG.md"]]
    files += [p for folder in ["skills", "assets"] for p in (root / folder).rglob("*") if p.is_file()]
    files.sort(key=lambda path: path.relative_to(root).as_posix())
    if any(p.is_symlink() for p in files):
        raise ValueError("archive cannot contain symlinks")
    destination.mkdir(parents=True, exist_ok=True)
    prefix = package["name"] + "-" + package["version"]
    archive = destination / (prefix + ".zip")
    if archive.exists():
        raise ValueError("archive already exists: choose an empty destination")
    hashes = {}
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for path in files:
            relative = path.relative_to(root).as_posix()
            data = path.read_bytes()
            entry = zipfile.ZipInfo(package["name"] + "/" + relative, date_time=date)
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            output.writestr(entry, data, compresslevel=9)
            hashes[relative] = hashlib.sha256(data).hexdigest()
    manifest = destination / (prefix + ".manifest.json")
    write_json(manifest, {"name": package["name"], "version": package["version"], "repository": package["repository"], "commit": commit, "archive": archive.name, "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(), "skills": package["extensions"][EXTENSION]["skillCount"], "files": hashes})
    submission = destination / (prefix + ".submission.md")
    submission.write_bytes((root / "docs/submission.md").read_bytes())
    assets = [archive, manifest, submission]
    (destination / "SHA256SUMS").write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name + "\n" for p in assets), encoding="utf-8")
    with zipfile.ZipFile(archive) as check_zip:
        if check_zip.testzip() is not None or len(check_zip.namelist()) != len(files):
            raise ValueError("archive integrity check failed")
    print(f"Built {archive.name} from {commit} ({archive.stat().st_size} bytes)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["sync", "check", "build"])
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    if args.command == "sync":
        synchronize(ROOT)
    elif args.command == "check":
        check(ROOT)
    else:
        build(ROOT, args.dist)


if __name__ == "__main__":
    main()
