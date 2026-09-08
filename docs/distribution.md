# Install, update, and roll back

The source is `skills/`. Each folder contains unchanged skill instructions and
an MIT license notice. The root `plugin.json` is the version authority; native
Claude and Codex manifests are generated from it. A package version identifies
one snapshot of all skills, while installation can select a subset.

## Reproducible standalone installation

Skills CLI 1.5.25 needs Node.js >=22.20.0. The skills themselves do not require
Node.js. Install into the current project and commit the files and lock record:

```sh
npx skills@1.5.25 add "Dankosik/rust-cli-skills#v1.0.0" --agent codex --skill '*' --copy
```

For a subset, replace `'*'` with names such as `rust-implement`. For Claude standalone
placement, use `--agent claude-code`. The `#v1.0.0` suffix is a Git ref; `@...`
after a repository is not the same version syntax. A full commit SHA can replace
the tag. Do not combine `--all` with a one-agent intention: that flag selects
all supported agent destinations.

GitHub CLI 2.97.0 offers a preview alternative:

```sh
gh skill install Dankosik/rust-cli-skills rust-implement --pin v1.0.0 --agent codex --scope project
gh skill update --dry-run
```

GitHub CLI injects source metadata into installed frontmatter. Its normal update
skips pinned skills. See its current help before intentionally changing that pin.
Use one manager for a given installed copy.

## Native Claude Code plugin

```sh
claude plugin marketplace add Dankosik/agent-skills-marketplace
claude plugin install rust-cli-skills@dankosik-skills
```

Inside Claude Code, the same commands start with `/plugin`. Plugin skills have
a namespace, for example `/rust-cli-skills:rust-implement`. Refresh the catalog and
update this plugin when you choose to adopt a new release:

```sh
claude plugin marketplace update dankosik-skills
claude plugin update rust-cli-skills@dankosik-skills
```

Restart or reload plugins as directed by the client. Native plugin managers may
have automatic-update settings; use project-vendored, pinned files for a workflow
that requires an explicitly reviewed update PR.

## Native Codex plugin

```sh
codex plugin marketplace add Dankosik/agent-skills-marketplace
codex plugin add rust-cli-skills@dankosik-skills
```

The author marketplace is a separate source in the plugin interface. It is not
an assertion of acceptance into OpenAI's curated public directory. To refresh:

```sh
codex plugin marketplace upgrade dankosik-skills
codex plugin add rust-cli-skills@dankosik-skills
```

Start a new task after installing or updating, so it sees the new plugin state.
These CLI forms are verified against Codex CLI 0.153.4; client capabilities can
change. Do not install a native pack and a standalone copy of the same skills
into the same workflow unless you intentionally want duplicate entries.

## Updates and rollback

For a working project, update on a branch to an explicit newer release, inspect
the instruction diff, run focused checks for changed behavior, and commit the
installed files plus installer metadata together. Roll back that change with
Git. Do not make an agent startup silently fetch main.

The author catalog pins exact package commits. To roll back a native plugin,
use the desired immutable marketplace snapshot or install the older standalone
release after removing the conflicting native copy. Never move an upstream tag.
A published package version and its assets are immutable.

## Publication and validation

Python 3.12 and `requirements-dev.txt` are authoring/CI requirements only.
The archive contains skill folders, license notices, manifests, logo, README,
privacy/support information and changelog; it excludes authoring scripts and CI.
`SHA256SUMS` and the release manifest record its bytes and source commit.

```sh
python -m pip install -r requirements-dev.txt
python scripts/distribution.py sync
python scripts/distribution.py check
python -m unittest discover -s scripts/tests
python scripts/install_smoke.py
```

The validation uses the official Agent Skills reference at a fixed commit and
the published Agent Plugins 1.0.0 schema. Native client checks supplement those
structural checks; none establishes universal behavioral quality. See
[versioning](versioning.md) and [submission materials](submission.md).

Sources: [Agent Skills](https://agentskills.io/specification),
[Agent Plugins](https://agent-plugins.org/plugin-authors/manifest),
[Skills CLI](https://github.com/vercel-labs/skills),
[GitHub CLI](https://cli.github.com/manual/gh_skill_install),
[Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces),
[OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins).
