# Executable instruction-evaluation fixtures

Status: **three executable tasks; no model comparisons recorded**. This is
maintainer tooling, not a dependency of any installed skill. Python 3.11+ is
needed for the harness; a preinstalled Cargo toolchain and POSIX process groups
are needed to execute Rust artifacts. No packages, models, credentials, network
services, or toolchains are installed by this harness.

## What is checked

| Task | Independent artifact oracle | Still requires trace/manual evidence |
| --- | --- | --- |
| R01 | Built CLI: inclusive endpoints, equal bounds, signed extremes, order/duplicates, empty selections, invalid range and invalid input; exact streams/status | Whether the agent completed its own checks, retained useful regression tests, and avoided unrelated edits |
| R05 / E05 | Direct Read/Write: arbitrary bytes, CRLF, NUL, final records, short reads/writes, error propagation and byte counts | Streaming/retention analysis, scope, actual skill loading; no OS pipe/PTY claim |
| R06 | Direct Write: late flush failure, successful/empty completion, short writes, partial-write errors and WriteZero | Process exit status and actual pipe behavior are not exercised |

The [catalogue](cases.json) has three implicit/contextual executable tasks, one
explicit variant (E05), and eight manual negative/contextual controls. Manual
controls are deliberately narrower than the wider
[20 scenario specifications](../docs/behavioral-scenarios.md). The current
[comparison protocol](../docs/behavioral-evaluation.md) and
[results template](../docs/evaluation-results-template.md) govern real model trials.

## Prepare a trial

From the author checkout, choose a destination **outside** it that does not exist:

```sh
python evals/run.py prepare R05 /tmp/rust-skill-trial-r05
```

This copies only the fixture's Cargo files, source, README and gitignore. The JSON
response supplies the natural prompt and fixture hash. Present that prompt and
workspace to the agent, with the chosen instruction variant installed normally.
Do not give it `cases.json`, this author's AGENTS.md, oracles, or known repairs.
There is no call to Codex or another model inside `prepare` or `grade`.

Use fresh sessions for no pack, the prior pack at
`aa14d4147af6bb5b58533389cd2ba52455459790`, and the exact candidate commit. Keep
host/model, permissions, fixture, toolchain, selected trials and budgets pinned.
Capture visible tool actions and the final artifact outside the trial workspace.
Record `rustc --version --verbose` and `cargo --version` once per unchanged
comparison environment; a declared rust-version is not an MSRV test result.

For manual controls, present only the prompt from `python evals/run.py list`.
The other fields are evaluator-only rubric/coverage, not agent instructions.
Grade the visible response and actions; do not invent project files or an
execution trace that the control does not supply.

## Grade the resulting artifact

After stopping agent writes, run in a disposable, appropriately sandboxed host:

```sh
python evals/run.py grade R05 /tmp/rust-skill-trial-r05 > /tmp/r05-artifact.json
```

The grader rejects changed Cargo semantics, new build configuration, symlinks,
special source files, and oversized source trees. Harmless manifest formatting
is allowed. It copies candidate `src/` into a new temporary crate using the
trusted fixture manifest/lockfile and external oracle. Candidate tests, build
scripts, and Cargo configuration are not executed. Thus the artifact result
cannot certify the candidate's own tests or the original project's whole suite.

Builds use one Cargo job, locked/offline resolution, and isolated Cargo storage.
The default build deadline is 30 seconds (`--timeout` overrides it); each oracle
process is capped at 5 seconds or the smaller supplied deadline. Captured log
bytes are bounded at 256 KiB. The supervisor terminates the POSIX process group
and waits for its direct child, including on timeout or excess output. Completion
records detect an oracle that exits early without finishing its assertions.

This is **not a security sandbox**. Candidate Rust code still executes arbitrary
instructions. Compiler include paths, escaped/detached descendants, network,
CPU, memory, disk, and access to host files require OS-enforced isolation and
resource limits. Temporary directories, a curated environment, source screening,
and Cargo `--offline` do not provide those guarantees. The log-size monitor is
not a hard disk quota. Use a quiescent candidate snapshot; concurrent hostile
filesystem mutation is outside this harness's boundary.

Reports preserve raw output as hex, commands, source/fixture/oracle/grader hashes,
and the stage reached. Exit 0 means **artifact pass only**, exit 1 means artifact
failure, and exit 2 means blocked, incomplete, inapplicable, or invalid invocation.
Missing Cargo is blocked; a deadline or missing completion marker is incomplete;
a compilation failure is not a behavioral regression test. `behavior_result`
remains `not_assessed` until a human or separate evaluator reviews the actual
agent trace. A pass cannot excuse fabricated checks or unauthorized actions.

## Verify the evaluator itself

The existing repository test command discovers the harness checks:

```sh
python -m unittest discover -s scripts/tests -v
```

`test_evaluation.py` checks preparation, rubric isolation, scope boundaries,
byte capture, bounded execution, and honest result classification. If Cargo and
POSIX are available, it also grades each known-broken fixture, requires failure
**at the oracle rather than compilation**, applies the corresponding known repair
in a temporary copy, and requires a pass. It never calls a model. Without that
environment the Rust sensitivity check explicitly skips; skip is not a pass.

`repairs/` exists only to verify oracle sensitivity. Never install it into an
agent trial. Do not modify the oracle to accommodate a failing candidate without
first demonstrating that the task contract or oracle itself is wrong. These
small known-defect checks validate the evaluation mechanism, not an assertion
that the candidate skills improve model behavior or cover every Rust CLI risk.
