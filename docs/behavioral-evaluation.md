# Behavioral evaluation — Rust CLI instructions

Status: **three executable tasks; model comparisons NOT RUN**. R01, R05, and
R06 now have checked-in Cargo fixtures and independent artifact oracles. The
remaining wider scenarios are specifications, not executed tests. This document
is the current authoring protocol, not an installed skill dependency or a
mandatory workflow for users of the pack.

The original [20-case specifications](behavioral-scenarios.md) are retained
byte-for-byte from `aa14d4147af6bb5b58533389cd2ba52455459790` as a historical
source. Their opening status and comparison instructions describe that earlier
snapshot; use the current protocol here and the executable catalogue below for
new comparisons. The earlier `009ede5` instructions may remain an additional
historical baseline, but are not a substitute for the immediate prior revision.

## Comparison protocol

Compare no pack, the prior pack at
`aa14d4147af6bb5b58533389cd2ba52455459790`, and the candidate's exact commit. Keep
the fixture, model, host, reasoning settings, permissions, toolchain, target,
dependencies, commands, and resource budgets identical within each trial. Use
fresh sessions and clean copies without outcomes leaking between runs. Select
cases and repeated-trial counts before looking at results. Evaluate models
separately; one host/model result does not establish a universal benefit.

A fixture needs source, a manifest and lockfile where appropriate, independent
expected outcomes, representative bytes, known failing/passing checks, concrete
bounds, and environment requirements. Pin its commit or content hashes and the
oracle independently. Do not ask the agent under evaluation to create its own
acceptance oracle. The [executable subset](../evals/README.md) supplies this for
three tasks; new filesystem, process, terminal, and concurrency cases require
the actual named mechanism rather than an approximate replacement.

Present only the natural prompt, pinned fixture, and normal project instructions.
Withhold expected skills, acceptance rubric, independent oracles, and known
repairs. Run outside this author's checkout so its maintenance AGENTS.md and
reference documents do not contaminate the consumer task. Isolate all effects;
no production access, user secrets, publication credentials, or global installs
are required. Untrusted candidate execution requires an actual OS sandbox, not
merely a temporary directory or Cargo `--offline`.

Grade correctness and authorized scope first: bytes, errors, status, side effects,
cleanup, and honest evidence. Then assess unnecessary questions, first-patch
stopping, unrelated edits, repeated checks, loaded skills, tool calls, elapsed
time, and context usage where available. Lower cost is not a win when correctness
or safety regresses. Multiple relevant skills may be appropriate. Judge visible
actions and artifacts, not private reasoning, magic phrases, or exact tool order.

Use the [results template](evaluation-results-template.md). Keep artifact results
separate from visible behavior/scope results. A passing artifact cannot excuse
fabricated checks or unauthorized actions. Record blocked, skipped, incomplete,
and not-run cases separately from pass/fail. Missing tools and exhausted budgets
are unavailable evidence, not clean verdicts. Keep all preselected trials.

Before asserting that an instruction change improves agent behavior, run its
relevant real model cases and near-misses. Structural CI proves packaging, and
known-defect/known-repair checks prove the oracle's sensitivity; neither is a
model comparison. Record these evidence classes separately.

## Coverage map

The [machine-readable catalogue](../evals/cases.json) contains 12 prompts: three
executable tasks, one explicit-invocation variant using the R05 oracle, and eight
manual routing/scope controls. It does not automate all scenarios below. Manual
controls without project fixtures assess only the evidence their prompts supply.

| Wider scenario | Current executable coverage |
| --- | --- |
| R01 — Inclusive range, completion, and scope | Artifact oracle: built binary bytes/status. Completion and scope still need a real trace. |
| R02 — Ownership/abstraction review stays read-only | Specification; N02 is a narrower manual Arc-sharing control. |
| R03 — Parser/configuration precedence, no unnecessary PTY | Specification; N03 is a narrower pure-merge control, not a parser fixture. |
| R04 — Help avoids config and child effects | Specification only. |
| R05 — Raw bytes and final unterminated record | Direct Read/Write artifact oracle; E05 repeats it with explicit invocation. |
| R06 — Late flush failure | Direct Write artifact oracle, not process-status proof. |
| R07 — Stream-specific BrokenPipe | Specification; C07 is a manual policy/evidence control, not a real-pipe test. |
| R08 — Record limit enforced while reading | Specification only. |
| R09 — Non-UTF-8 read-only traversal | Specification only; needs its platform filesystem. |
| R10 — Alias protection and staged replacement | Specification only; ordinary success would not prove crash durability. |
| R11 — Child pipes, stdin EOF, status, and reaping | Specification only; needs controlled child processes. |
| R12 — Blocking-worker cancellation observes completion | Specification; C12 is a manual diagnosis control, not worker execution. |
| R13 — Slow-first ordered results stay bounded | Specification only; needs coordinated work and explicit bounds. |
| R14 — Shared-view retention, no invented RSS | Specification; N04 is a narrower fabricated-evidence control. |
| R15 — Agreed buffer/cap, no compulsory profiler | Specification only. |
| R16 — Performance audit without measurements | Specification only. |
| R17 — MSRV and default features | Specification only; declared Rust versions are not compatibility evidence. |
| R18 — Profile-specific diagnosis | Specification only. |
| R19 — Preparation is not publication | Specification; N05 is a manual authority control, not an installer test. |
| R20 — Miri does not certify arbitrary OS soundness | Specification only. |

N01 additionally tests unrelated Rust-keyword activation, and N06 tests fixture
text that attempts to redirect the agent. Retain the original negatives from
[submission](submission.md). A scenario's presence in any catalogue is not an
observation that a model passed it.
