# Behavioral evaluation results — template

Status: **NOT RUN**. This empty template is not an evaluation report. Copy it for
an actual comparison; do not replace missing observations with expected outcomes.
Follow [the protocol](behavioral-evaluation.md).

## Reproducibility

| Field | Recorded value |
| --- | --- |
| Date and evaluator | Not recorded |
| No-pack / prior / candidate instruction revisions | Not recorded |
| Fixture repository commit or content hashes | Not recorded |
| Model, host, and versions | Not recorded |
| Reasoning settings, permissions, and tool availability | Not recorded |
| Rust edition, toolchains, MSRV, target, profile, features, Cargo.lock hash | Not recorded |
| OS, available process/PTY/filesystem facilities, resource limits | Not recorded |
| Selected cases, trial count and sampling plan chosen before running | Not recorded |
| Input hashes, commands, output destination, cache conditions where relevant | Not recorded |

## Observations

| Case / trial | Variant | Result | Evidence and artifact references | Scope / correctness issue | Unverified boundary |
| --- | --- | --- | --- | --- | --- |
| Not run | Not run | Not run | None | Not assessed | Not assessed |

Use pass, fail, blocked, skipped, or not run explicitly. Record output bytes,
status, side effects and cleanup relevant to each case. Include original
submission negatives when evaluating activation and honesty. Record observable
skill loads, tool calls, elapsed time, and context use only if available; never
infer them from guesses or private reasoning.

## Interpretation

Separate correctness and scope regressions from cost changes. Identify evidence
supporting each conclusion, trial variability, environmental limitations, and
unexecuted cases. Do not infer whole-program speed or memory gains from improved
agent traces; those require separate program measurements. Do not generalize a
single model/host result to all consumers of the pack.

Decision on the candidate and reason: **not assessed**.
