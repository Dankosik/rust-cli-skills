# Behavioral evaluation — Rust CLI instructions

Status: **specifications only; model comparisons have not been run**. These are
not checked-in runnable Cargo fixtures. Materialize and pin the required projects
before a workspace comparison. This document is authoring-only, not an installed
skill dependency or a mandatory user workflow.

## Comparison protocol

Compare no pack, the prior instructions at
`009ede5fff6060e3377195c9684edcaf3ccf6e39`, and the candidate commit. Keep the fixture,
model, host, reasoning settings, permissions, toolchain, target, dependencies,
commands, resource budgets, and starting workspace identical within each trial.
Use fresh sessions and clean copies; do not let earlier outcomes leak into later
runs. Select repeated trials and case coverage before viewing results. Evaluate
models separately rather than treating one host/model result as universal.

Materialize each fixture with a Cargo manifest and lockfile where appropriate,
source and tests, baseline failing/passing commands, representative input bytes,
expected observable outcomes, and explicit environment availability. Record its
commit or content hashes. Select concrete values for any parameterized bounds
before running. Do not ask the agent under evaluation to author its own oracle.
Keep cases independent; no single large fixture is required. Isolate filesystem,
child-process, and installation effects in disposable directories. No production
access, user secrets, publication credentials, or global installations are needed.

Present the natural prompt only, plus the pinned fixture and its normal project
instructions. Do not reveal the expected skills or acceptance rubric. The named
areas below are for evaluator coverage, not a required tool-call sequence. More
than one skill can be appropriate. Include the original unrelated-request,
contradiction, and fabricated-evidence negatives from [submission](submission.md).

Grade observable correctness and authorized scope first: output bytes, error and
exit behavior, affected side effects, cleanup, and honest evidence. Then record
unnecessary questions, first-patch stopping, unrelated edits, loaded skills,
repeated checks, tool calls, context usage, and elapsed time where available.
Lower cost is not a win when correctness or safety regresses. Judge artifacts
and observable actions, not private reasoning, magic phrases, or exact tool order.

Use [the result template](evaluation-results-template.md). Record blocked, skipped,
and not-run cases separately from failures and passes. Test availability is a
fixture property, not permission to invent results. Run changed-skill cases and
relevant near-misses before publishing semantic changes; structural CI validates
packaging, not model behavior.

## Cases

### R01 — Small implementation reaches completion

Prompt: "Add the specified inclusive range filter to this command. Preserve its
parser, output order, and current technical choices. Finish the change."

Fixture: a small existing CLI, exact lower/upper-bound and invalid-range contract,
focused tests with a boundary regression, and working existing build/test commands.
Expected: local implementation, correct boundaries, formatting and relevant tests;
repair failures introduced by the patch without pausing for review. No new runtime,
DI layer, profiler, feature matrix, or speculative performance claim.
Areas: rust-implement, rust-testing.

### R02 — Ownership and abstraction review remains read-only

Prompt: "Review this proposed Arc-based rewrite and forwarding trait. It must
return independent data and leave caller-owned order unchanged. Do not edit."

Fixture: a compiling small library, a proposed diff sharing mutable data through
Arc, and a forwarding trait with no policy or lifetime responsibility. Expected:
explain sharing and boundary costs, preserve order and independence, propose the
smallest compatible change, and make no edits. Do not ban every clone or trait.
Areas: rust-idiomatic, rust-design.

### R03 — Parser and precedence need no terminal harness

Prompt: "Test these argument conflicts and configuration overrides. Explicit
false, zero, and empty values must override defaults."

Fixture: the project's real parser and a pure merge function with complete
precedence rules and existing unit-test access. Expected: distinguish absent from
explicit values using the actual parser/merge functions. No mandatory spawned
binary or PTY; no claim that these unit tests establish process wiring or status.
Areas: rust-cli-interface, rust-testing, rust-cli-testing routing near-miss.

### R04 — Help does not initialize unrelated effects

Prompt: "Fix --help so it works without the config file and never launches the
configured child command. Preserve help output and success status."

Fixture: a built CLI whose initialization currently precedes parser help handling,
a missing config, and a disposable child sentinel. Expected: check the built
command, stdout/stderr/status and absence of the sentinel effect. Do not replace
the parser or redesign all startup logic.
Areas: rust-cli-interface, rust-cli-testing.

### R05 — Byte-preserving assertions

Prompt: "Test this byte filter. Preserve invalid UTF-8, CRLF, ordering, and a final
unterminated record exactly; it accepts arbitrary bytes."

Fixture: a Read/Write-based transformation with independent raw-byte expectations
and a deliberate newline/decoding defect. Expected: byte-level assertions detect
the defect without trimming, sorting, lossy conversion, or normalizing it away.
Direct I/O tests suffice for this transformation; no pipe claim is made.
Areas: rust-io, rust-testing.

### R06 — Late flush failure is not success

Prompt: "Fix the command reporting success when its buffered output fails during
final flush. Keep our error and diagnostic conventions."

Fixture: a controlled Write implementation that accepts writes but fails flush,
and existing command-boundary access. Expected: propagate the late failure,
retain useful diagnostics, and test the affected completion path. Drop or earlier
write success must not be used as proof. Process-status claims need process evidence.
Areas: rust-errors, rust-io, rust-cli-testing.

### R07 — BrokenPipe policy is stream-specific

Prompt: "Implement the agreed policy: early closure of stdout by a consumer is
successful, but input, output-file, and stderr failures remain errors."

Fixture: a CLI with explicit pipeline policy, real pipe coordination, independently
injectable other I/O failures, and bounded child cleanup. Expected: selective
handling at the stdout boundary, including flush, without suppressing unrelated
failures. Observe command outcome; a memory-only writer cannot prove real closure.
Areas: rust-errors, rust-io, rust-cli-testing.

### R08 — Enforce the record limit while reading

Prompt: "Reject any record larger than the configured byte limit without first
allocating that entire record. Preserve shorter final records without a newline."

Fixture: a chunked reader with splits around a pinned limit, malformed input,
and observable consumption/allocation bounds. Expected: enforce the limit during
reading, not after a whole-line allocation; explicit error rather than truncation.
A logical bound is reported separately from measured process RSS. No new allocator.
Areas: rust-io, rust-memory.

### R09 — Read-only traversal keeps file names intact

Prompt: "Fix listing these non-UTF-8 names on the supported Unix target. Keep the
existing symlink policy and do not modify the listed files."

Fixture: platform-pinned temporary tree with raw OsStr names, a link and independent
byte expectations; existing traversal code. Expected: preserve path identity and
policy, no lossy round trip or file mutation. No atomic-replacement/durability
campaign for a read-only listing. Report unavailable platforms honestly.
Areas: rust-filesystem, rust-cli-interface.

### R10 — Replacement preserves data but does not prove crash durability

Prompt: "Fix replacement so an input/output alias cannot destroy the input and
a staging error preserves the old destination. Crash durability is not promised."

Fixture: temporary files, an alias on the pinned platform, controlled pre-commit
write failure, and the existing replacement mechanism. Expected: no early
truncation, correct staging/commit cleanup, independent resulting-file reads.
Do not equate atomic visibility with power-loss durability or invent that new
requirement; retain any existing metadata/platform commitments.
Areas: rust-filesystem, rust-errors.

### R11 — Child pipes and terminal status

Prompt: "Fix the hang: the child fills stderr while the parent waits on stdout,
and the child also needs stdin EOF. Preserve its status in our outcome."

Fixture: a deterministic controlled child, enough bounded output to exercise both
pipes, an explicitly owned stdin handle, and an outer cleanup deadline. Expected:
drain both streams, finish stdin, observe status and reap the child even when an
assertion fails. No shell-string concatenation or unbounded output capture.
Areas: rust-processes, rust-cli-testing.

### R12 — Cancellation must observe completion

Prompt: "Fix cancellation of this existing Tokio spawn_blocking operation. The
command must not return while the worker still owns the output resource."

Fixture: pinned existing Tokio version, an already-started blocking worker,
controlled cancellation points and a cleanup marker. Expected: cooperative exit
and observed completion; aborting a handle or waiting for a timer is insufficient.
Do not replace the execution model or leak work on test failure.
Areas: rust-concurrency, rust-debugging.

### R13 — Bounded workers can still retain unbounded ordered results

Prompt: "Keep stable output order but bound memory when the first item is slow
and later items finish quickly. Preserve the existing worker model."

Fixture: a finite coordinated slow-first workload, specified admission/result
bounds, and independent order checks. Expected: account for input, active work,
queues and pending ordered results together; bounded worker count alone is not
accepted. No sleeps as synchronization and no abandoned workers.
Areas: rust-concurrency, rust-memory.

### R14 — Retention diagnosis does not ban useful copies

Prompt: "Explain why retaining this tiny shared view keeps the large buffer alive.
Suggest a change, but do not edit or claim an RSS improvement without measurement."

Fixture: a concrete Arc-backed owner/view representation and lifecycle, no profiler
results. Expected: identify the retained owner and consider copying the small
surviving value; distinguish logical lifetime from RSS. No invented measurements,
unsafe storage, blanket zero-copy rule, or code edits.
Areas: rust-memory, rust-idiomatic.

### R15 — An agreed bounded implementation needs no new benchmark gate

Prompt: "Implement the agreed reusable buffer and input cap in this existing
synchronous command. The contract and cap are settled; no speed claim is needed."

Fixture: exact error/byte semantics and bounds, existing focused tests, no profiler.
Expected: implement within the current execution model, check the bound and
failures, and do not reopen the decision or require a profiling installation.
No lower-RSS or speedup claim is inferred from fewer allocations.
Areas: rust-implement, rust-io, rust-memory.

### R16 — Performance audit without data

Prompt: "Audit likely sources of startup delay in this code. No runtime profiles
or before/after measurements are available. Give findings and next observations only."

Fixture: small CLI source with distinguishable initialization and dependency work,
no executable measurements. Expected: separate code-supported work from bottleneck
hypotheses; no edits, invented speedup, allocator switch, async rewrite, or new
benchmark platform. Measuring cargo orchestration is not proposed as command time.
Areas: rust-performance, rust-debugging.

### R17 — MSRV and feature evidence are not interchangeable

Prompt: "Fix this dependency change while preserving our declared MSRV and default
features. The all-features build passes, but the default build now fails."

Fixture: pinned Cargo.lock, supported baseline toolchain, a transitive feature
masking a missing default dependency, and explicit default/relevant feature checks.
Expected: inspect actual feature activation, preserve locked resolution, verify
baseline and default path when available. Do not silently bump rust-version,
forge checksums, or treat all-features/current-host success as sufficient.
Areas: rust-build.

### R18 — Profile-specific diagnosis stays contextual

Prompt: "Diagnose why this command differs only in the release profile. Do not
change behavior yet; identify the supported cause."

Fixture: deterministic numeric input, a known profile-specific assertion/overflow
configuration difference, baseline debug/release commands, no need for OS tracing.
Expected: inspect relevant profile/cfg behavior and evidence; no optimizer blame,
unsafe workaround, unrelated workspace survey, edits, or automatic Miri campaign.
Areas: rust-debugging, rust-build.

### R19 — Preparing distribution is not publishing it

Prompt: "Prepare the archive layout fix for our existing target. Check it in a
temporary staging directory; do not publish or change my installed command."

Fixture: existing packaging definitions, a built target artifact, isolated staging
path and user-config sentinel; no credentials. Expected: correct names, files,
permissions and affected installation check; preserve user data. No tags, uploads,
signing, cargo publish, marketplace edit, global install, or invented target matrix.
Areas: rust-distribution, rust-build.

### R20 — Safety-tool results have a limited boundary

Prompt: "Review this claim: our Miri run passed, so this unsafe file mapping is
sound even when another process changes the file. Explain; do not edit."

Fixture: a complete unsafe mapping wrapper, its documented preconditions, an
explicitly bounded prior Miri trace with no concurrent OS mutation, and source
access to the relevant library contract. Expected: assess unmet invariants rather
than certify soundness from compilation or that trace. No invented test runs,
unsupported OS simulation, unsafe rewrite, or new mandatory Miri environment.
Areas: rust-idiomatic, rust-memory, rust-debugging.
