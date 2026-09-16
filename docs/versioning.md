# Versioning and releases

The root `plugin.json` is the package identity and version authority. One SemVer
version covers this repository; other language packs release independently.
Skill names, paths, scope, invocation expectations and required environment form
the public contract. PATCH corrects behavior within that contract; MINOR adds
compatible capabilities; MAJOR changes or removes an existing contract.
A description change can affect activation and is not automatically cosmetic.

Update `plugin.json` and CHANGELOG.md, then run `python scripts/distribution.py sync`.
The native manifests are derived views; CI rejects version or metadata drift.
Skill files do not receive a package-version bump just to change their hashes.

Run `python scripts/distribution.py check` and the installation smoke command
in docs/distribution.md. CI validates the format and distributable; semantic
skill changes additionally need focused behavioral evaluation. An installation
pass is not proof of quality across all models.

The 1.0.1 candidate corrects task scope and completion within existing domains;
names, paths, independent installation, and environment contracts are unchanged.
This is a PATCH correction, not an assertion that description edits are merely
cosmetic. Broader future activation or scope changes still need a fresh SemVer
assessment.

Use the [evaluation protocol](behavioral-evaluation.md) to select changed cases
and routing negatives. Record concrete fixture revisions, model/host settings,
observed outcomes, and unexecuted cases using the
[results template](evaluation-results-template.md). Structural CI and a set of
proposed scenarios are not substitutes for focused behavioral evidence before
publishing semantic changes.

Keep a prepared version explicitly unreleased until its immutable tag and assets
exist; leave installation examples pinned to the last published release in the
meantime. Preparing metadata does not authorize publication or marketplace edits.

Release from a reviewed, green commit. Push `vX.Y.Z` matching plugin.json.
The release workflow validates that exact tag, builds one skills-only archive,
records file hashes and commit identity, and uploads all assets before publishing.
Enable GitHub release immutability in repository settings. Published versions
and their assets must never be replaced; corrections receive a new version.

The author marketplace pins each pack's release commit. After a release, update
that catalog's ref and SHA in a reviewed change. Claude versions affect cache
updates; always bump the native plugin version with the release. Do not put a
second version in the marketplace entry. Consumers use one manager per installed
copy and review instruction changes before updating a working project.
