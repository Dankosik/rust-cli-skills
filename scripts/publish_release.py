#!/usr/bin/env python3
"""Publish a checked asset set, or verify an identical existing release."""

import hashlib
import json
import os
from pathlib import Path
import subprocess


def gh(*args, missing_ok=False):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode:
        try:
            payload = json.loads(result.stdout)
        except ValueError:
            payload = {}
        if missing_ok and str(payload.get("status")) == "404":
            return None
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return json.loads(result.stdout) if result.stdout.strip().startswith(("{", "[")) else result.stdout.strip()


def verify_assets(release, expected, complete):
    assets = {asset["name"]: asset for asset in release["assets"]}
    if len(assets) != len(release["assets"]) or set(assets) - set(expected):
        raise ValueError("release contains duplicate or unexpected assets")
    for name, asset in assets.items():
        if asset.get("digest") != "sha256:" + expected[name]:
            raise ValueError("published/draft asset differs from this candidate: " + name)
    if complete and set(assets) != set(expected):
        raise ValueError("published release is missing candidate assets")
    return set(expected) - set(assets)


def main():
    root = Path(__file__).resolve().parents[1]
    package = json.loads((root / "plugin.json").read_text())
    repo = os.environ["GITHUB_REPOSITORY"]
    tag = os.environ["RELEASE_TAG"]
    if package["repository"] != "https://github.com/" + repo or tag != "v" + package["version"]:
        raise ValueError("release target differs from package identity")
    paths = {p.name: p for p in (root / "dist").iterdir() if p.is_file()}
    manifest = json.loads(next((root / "dist").glob("*.manifest.json")).read_text())
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    if manifest["commit"] != head:
        raise ValueError("built release is not from the current candidate")
    refs = subprocess.check_output(["git", "ls-remote", package["repository"] + ".git", "refs/tags/" + tag, "refs/tags/" + tag + "^{}"], text=True)
    refs = {line.split()[1]: line.split()[0] for line in refs.splitlines()}
    if refs.get("refs/tags/" + tag + "^{}", refs.get("refs/tags/" + tag)) != head:
        raise ValueError("remote tag does not identify this candidate")
    expected = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}
    endpoint = "repos/" + repo + "/releases/tags/" + tag
    release = gh("api", endpoint, missing_ok=True)
    if release and not release["draft"]:
        verify_assets(release, expected, complete=True)
        print("Identical release already published; no mutation needed.")
        return
    if release is None:
        gh("release", "create", tag, "--repo", repo, "--verify-tag", "--draft", "--target", head, "--title", tag, "--notes-file", str(root / "docs/release-notes.md"))
        release = gh("api", endpoint)
    missing = verify_assets(release, expected, complete=False)
    if missing:
        gh("release", "upload", tag, *[str(paths[name]) for name in sorted(missing)], "--repo", repo)
    release = gh("api", endpoint)
    verify_assets(release, expected, complete=True)
    gh("release", "edit", tag, "--repo", repo, "--draft=false", "--latest")
    published = gh("api", endpoint)
    if published["draft"]:
        raise ValueError("release remains a draft")
    verify_assets(published, expected, complete=True)
    print(published["html_url"])


if __name__ == "__main__":
    main()
