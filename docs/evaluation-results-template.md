# Behavioral evaluation results — template

Status: **NOT RUN**. This empty template is not an evaluation report. Copy it for
an actual comparison; do not replace missing observations with expected outcomes.
Follow [the protocol](behavioral-evaluation.md). The [artifact grader](../evals/README.md)
does not launch a model or establish an overall behavioral verdict.

## Reproducibility

| Field | Recorded value |
| --- | --- |
| Date and evaluator | Not recorded |
| No-pack / prior / candidate instruction revisions | Not recorded |
| Fixture repository commit or content hashes | Not recorded |
| Independent oracle revision/hash; grader command/version | Not recorded |
| Model, host, and versions | Not recorded |
| Reasoning settings, permissions, and tool availability | Not recorded |
| Rust edition, toolchains, MSRV, target, profile, features, Cargo.lock hash | Not recorded |
| OS, available process/PTY/filesystem facilities, resource limits | Not recorded |
| Selected cases, trial count and sampling plan chosen before running | Not recorded |
| Input hashes, commands, output destination, cache conditions where relevant | Not recorded |
| Fresh-session isolation and rubric/oracle withholding | Not recorded |

## Observations

| Case / trial | Variant | Artifact result | Visible behavior / scope result | Trace and artifact references | Unverified boundary |
| --- | --- | --- | --- | --- | --- |
| Not run | Not run | Not run | Not assessed | None | Not assessed |

Use pass, fail, blocked, skipped, incomplete, or not run explicitly. Record output
bytes, status, side effects, and cleanup relevant to each case. Retain failed and
unavailable preselected trials. An artifact pass cannot override an unauthorized
edit or fabricated evidence. Include original submission negatives and the
catalogue's near-misses when evaluating activation and honesty.

Record observable skill loads, tool calls, unnecessary questions, repeated checks,
elapsed time, and context use only when available. Leave unavailable metrics null;
never infer them from guesses, final-answer claims, or private reasoning. A
supervisor deadline or missing test-completion record is incomplete, not a pass.

## Interpretation

Separate correctness and scope regressions from cost changes. Identify evidence
supporting each conclusion, trial variability, environmental limitations, and
unexecuted cases. Do not infer whole-program speed or memory gains from improved
agent traces; those require separate program measurements. Do not generalize a
single model/host result to all consumers of the pack. Label packaging tests,
oracle mutation checks, independent review, and actual model trials separately.

Decision on the candidate and reason: **not assessed**.
