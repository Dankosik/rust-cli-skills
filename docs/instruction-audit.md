# Rust CLI instruction audit

Audited base: [009ede5fff6060e3377195c9684edcaf3ccf6e39](https://github.com/Dankosik/rust-cli-skills/tree/009ede5fff6060e3377195c9684edcaf3ccf6e39).
Scope: all 16 SKILL.md files, README, canonical/native manifests, distribution,
versioning, release/submission documentation, and the distribution checks that
constrain instruction packaging. No root AGENTS.md or CLAUDE.md exists at this
base. This is a static instruction audit, not observed model performance.

## Basis and decision

[OpenAI's September 11 article](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
recommends discriminating skill descriptions, contextual reading, fewer rigid
itineraries, and explicit completion boundaries, with attention to different
models consuming the same instructions. Applied here, this supports targeted
scope corrections rather than replacing compact technical skills with a new
orchestrator or deleting their Rust-specific safeguards.

Keep the 16 independently installable, single-file skills. The original README
already separates I/O flow, retained memory, workload performance, and process/OS
tests. Those are useful decisions, not redundant stages. Do not impose a fixed
skill sequence or one-skill maximum. Some repetition of scope boundaries remains
intentional because consumers can install one skill without the rest of the pack.
The goal is less unnecessary work, not a claim of fewer total words or measured
latency improvement.

## Main findings and changes

### 1. Activation and task mode

At the base, rust-idiomatic applies to writing values, functions, traits, and
transformations, overlapping ordinary implementation. Its finish criterion asks
for formatted code even when review is requested. rust-design, rust-debugging,
rust-memory, and rust-performance likewise tend toward a completed modification
or intervention. Several descriptions and submission examples explicitly permit
review or diagnosis, making that implied write scope undesirable.

Narrow overlapping descriptions around the decision needing guidance. Distinguish
review/diagnosis from editing, and benchmarking from optimization. Preserve settled
choices outside the explicitly requested change, rather than blocking a change
to a choice that the user actually requested. These are activation and behavior
corrections, not cosmetic wording changes.

### 2. Complete implementation without inventing new gates

rust-implement already gives autonomy on routine choices and rejects unsolicited
redesign. Clarify that the first patch is not the stopping point: complete the
appropriate existing formatting, compilation, and tests, repair introduced
failures, and reuse applicable results for the same revision and environment.
Required project checks still apply. A skill cannot assert that every user's
environment is disposable, safe to publish from, or authorized for external work.

A clear request ends when its result and required checks are satisfied, or with
a precise blocker. Platform matrices, profiling, Miri, new runtimes, unrelated
cleanup, and new test infrastructure do not become automatic gates. An unavailable
check must remain unverified, not be silently replaced with a weaker result.

### 3. Preserve distinct testing boundaries

A direct call to the real parser can establish grammar; it does not establish
executable wiring, exit status, or a terminal. Controlled Read/Write values can
establish short-operation and error propagation behavior, but not actual OS pipe
backpressure. Tests of built commands, pipes, PTYs, and platform filesystems are
chosen only when the changed property needs them. A cross-build is not runtime
validation on another platform. A pure flag or byte transformation change need
not create an unrelated process/PTY infrastructure project.

Keep raw-byte fidelity in tests, independently chosen expectations, meaningful
partial failures, and real cleanup. A passing snapshot is not permission to
normalize away the defect. These boundaries were largely present already; the
revision makes their defaults and scope more explicit.

### 4. I/O completion, file identity, and processes

Do not weaken late flush errors, stream-specific BrokenPipe policy, same-file
alias protection, or child lifecycle ownership. Standard-library
[BufWriter documentation](https://doc.rust-lang.org/std/io/struct.BufWriter.html)
notes that flush errors during destruction are ignored; completion-sensitive
errors must therefore remain observable. The
[Child documentation](https://doc.rust-lang.org/std/process/struct.Child.html)
explains that dropping std::process::Child does not stop it or automatically wait
for it. Qualify this as the standard-library type rather than assume all async
wrappers share its exact behavior.

Scope I/O checks to the changed read/write property. Read-only traversal does not
require crash-durability testing. When replacement is involved, preserve staging,
commit, metadata, and recovery requirements; do not equate atomic visibility with
crash durability. Argument-only subprocess changes need not run every interruption
scenario, but every child actually spawned in a test still needs bounded cleanup.

### 5. Resource analysis is not mandatory speculative optimization

Memory, CPU time, startup, allocation count, and RSS are not interchangeable.
Keep the original warning that a small shared view can retain a large owner;
copying a small surviving value can be more memory-efficient than retaining it.
Separate code-supported growth terms from measured memory results. An agreed
input cap or ownership change can be implemented without an invented profiler
gate, but it cannot be sold as an unmeasured RSS or speed improvement.

Concurrency remains bounded across admission, queues, active work, and ordered
results. Cancellation must observe termination, not just time out. The
[Tokio spawn_blocking documentation](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html)
confirms that abort does not cancel work once that blocking task has started.
Keep the execution model and cooperative cleanup; do not introduce async merely
because a CLI uses I/O. Runtime-specific behavior is named explicitly.

### 6. Cargo compatibility and publication authority

Replace rust-build's exhaustive workspace/toolchain/features/profile/environment
preflight with inspection of the affected Cargo layer. The
[Cargo Rust-version documentation](https://doc.rust-lang.org/cargo/reference/rust-version.html)
distinguishes the declared support contract and its verification. A newer compiler
is not evidence for an older baseline, and all-features success is not evidence
for the default path. Exercise affected configurations and required gates rather
than invent every feature combination or silently change MSRV or lint policy.

rust-distribution separates preparing/reviewing packaging from authorized
publication. Validate affected staging paths and artifacts without automatically
uploading, signing, changing tags, or modifying user-level installations. Preserve
owner-controlled credentials and the existing supported target set.

## Per-skill disposition

| Skill | Targeted correction | Technical content retained |
| --- | --- | --- |
| [rust-implement](../skills/rust-implement/SKILL.md) | Clear completion, relevant reuse, settled-change exception | Explicit ownership, bounded growing input, project baseline |
| [rust-idiomatic](../skills/rust-idiomatic/SKILL.md) | Decision-specific trigger; read-only review | Borrow/move meaning, Arc sharing, bytes, overflow, unsafe invariants |
| [rust-design](../skills/rust-design/SKILL.md) | Analysis vs refactoring | Small programs, meaningful traits, caller knowledge, resource ownership |
| [rust-cli-interface](../skills/rust-cli-interface/SKILL.md) | Parser/merge vs executable vs terminal checks | Cheap help, precedence, stdout/stderr, OsString, noninteractive policy |
| [rust-errors](../skills/rust-errors/SKILL.md) | Error-level vs process-level assertions | Typed causes, partial success, cleanup, stdout-specific BrokenPipe |
| [rust-io](../skills/rust-io/SKILL.md) | Changed read/write cases, no automatic benchmark | Short reads, record limits during reads, full writes, final flush |
| [rust-filesystem](../skills/rust-filesystem/SKILL.md) | Conditional traversal/replacement/durability | Paths vs identity, links, atomic creation, alias safety, staging |
| [rust-processes](../skills/rust-processes/SKILL.md) | Affected children; std::process qualification | Literal arguments, full pipes, stdin EOF, status and reaping |
| [rust-concurrency](../skills/rust-concurrency/SKILL.md) | Affected work; review vs change | Capacity, ordered buffering, locks, cooperative exit, joining |
| [rust-memory](../skills/rust-memory/SKILL.md) | Diagnosis, logical bound, measured reduction | Retained owners, capacity churn, stack/maps, adversarial hashing |
| [rust-performance](../skills/rust-performance/SKILL.md) | Audit, benchmark, authorized optimization | Optimized binary measurement, cache/output conditions, variance, CPU baseline |
| [rust-debugging](../skills/rust-debugging/SKILL.md) | Hypothesis-driven reads; diagnosis need not fix | Error chain, profile differences, ownership, Miri limitations |
| [rust-testing](../skills/rust-testing/SKILL.md) | Affected features; bounded optional advanced checks | Byte distinctions, I/O doubles, worker cleanup, real defect detection |
| [rust-cli-testing](../skills/rust-cli-testing/SKILL.md) | Parser unit-test distinction; scoped OS harness | Binary status, pipes vs PTY, fixture isolation, bounded capture |
| [rust-build](../skills/rust-build/SKILL.md) | Affected layer and configurations | MSRV, feature unification, lockfile integrity, profile and target contracts |
| [rust-distribution](../skills/rust-distribution/SKILL.md) | Preparation vs publication; no new target matrix | Linkage, CPU baseline, artifact provenance, user-owned data |

## Documentation, packaging, and evidence

Update README and CLI-specific default prompts through canonical plugin.json and
synchronized native metadata. Prepare 1.0.1 as an explicitly unreleased PATCH
within existing names, paths, independent installation, and environment contracts;
keep published installation commands pinned to v1.0.0. Do not move tags, publish
assets, or edit a marketplace as part of instruction maintenance.

The unchanged distribution validator permits only SKILL.md and LICENSE per skill.
Keep that contract. New audit and evaluation files live under docs for authors;
they are neither runtime dependencies nor additions to the shipped archive.
No global instruction file, new role, orchestration layer, toolchain dependency,
CI workflow, or packaging-script change is required.

The original submission has five positive examples naming a skill and three
negative examples. It does not establish natural routing or the full Rust CLI
boundary coverage. Retain those eight examples and add
[20 natural-request specifications](behavioral-evaluation.md), fixture-pinning and
comparison guidance, and an [unfilled results template](evaluation-results-template.md).
They are not executed model evaluations or runnable application fixtures.

Distribution validation, installation smoke checks, and archive tests establish
package properties only. Record actual CI separately from model evaluations.
Compare no pack, the pinned prior pack, and the candidate on controlled fixtures;
measure correctness and scope before cost. No speedup, lower generated-program
memory use, or universal cross-model benefit is asserted by this audit.
