# Reference-driven instruction review

Reviewed 2026-09-16 against base
[`aa14d4147af6bb5b58533389cd2ba52455459790`](https://github.com/Dankosik/rust-cli-skills/tree/aa14d4147af6bb5b58533389cd2ba52455459790).
All 16 skills were read. This is an authoring decision record, not an installed
skill dependency, a model-comparison result, or a certificate of perfection.
The [earlier audit](instruction-audit.md) remains a historical record of the
preceding change; its recommendations describe its own base, not this revision.

## Sources and selective transfer

| Primary source | Adopted here | Deliberately not copied |
| --- | --- | --- |
| [OpenAI: Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills), 2026-01-22 | Observable outcomes, independent artifact checks, implicit/explicit/contextual/negative prompts, fresh controlled comparisons | Treating substring matches or skill-name mentions as proof of correct behavior; claiming a catalogue is an executed evaluation |
| [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), 2026-09-11 | Decision-specific activation, conditional context, explicit completion, relevant rather than repeated checks | Fixed itineraries, mandatory all-file reading, or a universal claim across models |
| [Matt Pocock: writing-for-agents](https://github.com/mattpocock/skills/blob/959a8e9f1edc3adbe2f7e3054bb6fbefa6696260/skills/productivity/writing-for-agents/SKILL.md) | Precise context pointers, established concepts, co-located rules, completion criteria, pruning generic prose | A new glossary, compulsory setup, or splitting already compact self-contained skills into dependencies |
| [Matt Pocock: code-review](https://github.com/mattpocock/skills/blob/959a8e9f1edc3adbe2f7e3054bb6fbefa6696260/skills/engineering/code-review/SKILL.md) and [repository rationale](https://github.com/mattpocock/skills/tree/959a8e9f1edc3adbe2f7e3054bb6fbefa6696260) | Independent spec/standards axes when reviewers are available; behavior-sized feedback and meaningful red/green evidence | Mandatory interviews, another issue-tracker setup, universal smell findings, or serial self-review described as independent agents |
| [Alibaba: Open Code Review](https://github.com/alibaba/open-code-review/tree/f1101fd7f51304c82e4a4f292bbee88aea0823cf), especially its [skill](https://github.com/alibaba/open-code-review/blob/f1101fd7f51304c82e4a4f292bbee88aea0823cf/skills/open-code-review/SKILL.md) | Explicit scope and context, bounded work, evidence and location checks, omitted coverage reported separately | Mandatory OCR installation, API/provider dependencies, default worker counts, auto-publication, or wholesale copying its orchestration into each skill |
| [Thariq Shihipar: The new rules of context engineering](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models), 2026-07-24 | Remove stale/conflicting prescriptions, preserve useful interfaces and concrete code/test context, load relevant guidance | Arbitrary word-reduction targets or unsupported claims that pruning necessarily improves every model |

The supplied Alibaba URL ends with a Cyrillic character and returned 404; the
canonical repository above was verified. The supplied
[X article](https://x.com/trq212/article/2080710971228918066) could not be retrieved.
The Anthropic-hosted article by the same author is a separately verified primary
source, not an assertion that the unavailable X text was read or is identical.
No third-party implementation or prompt body is vendored into this MIT pack.

## Findings and changes

**Feedback can fail for the wrong reason.** The prior testing guidance required
meaningful assertions but did not explicitly distinguish a behavioral red test
from compilation failure or missing tooling. `rust-testing` and `rust-implement`
now require that distinction when a reproducer is available. Existing red evidence
can be reused; this does not impose new test infrastructure on every change.
R01, R05, and R06 provide independent executable oracles with known-defect checks.

**Review heuristics can become invented requirements.** `rust-design` now ties
material findings to code, callers, and a contract or concrete maintenance cost.
A design smell is a heuristic, not an automatic defect; a clean review is valid.
N02 and N03 check review-only scope; broader architecture claims still need
project-specific fixtures, not a canned universal smell score.

**A failed fix can lead to speculative patch stacking.** `rust-debugging` now
requires preserving the failure while minimizing a reproducer and choosing
observations that could disprove a hypothesis. It distinguishes unrelated baseline
failures. The wider R18 specification covers profile-specific diagnosis; C12
covers a termination near-miss. These are not executed model results.

**Shared verification needs one owner.** `rust-implement` and the maintenance
AGENTS.md preserve mandatory project checks while reusing applicable results and
assigning final aggregate checks to the integrating owner. They do not create an
agent team, force one skill per task, or weaken a check whose inputs changed.
R01's trace rubric covers completion and unrelated work, separately from its
executable oracle. Actual duplicate-check cost remains unmeasured.

**Evaluation existed only as prose.** The new [catalogue and harness](../evals/README.md)
provide three executable tasks, an explicit-invocation variant, and eight manual
controls. Independent oracle assertions are outside trial workspaces. They check
bytes, exit behavior, short writes, and late flush failures at named boundaries.
They do not pretend to automate all 20 wider scenarios or invoke a model.
A successful artifact check still needs trace/scope review for a model verdict.

**Authoring context was implicit.** The short root AGENTS.md records maintenance
constraints and conditional pointers. It is not included in installed skill
folders or release archives. It is not an extra runtime instruction file for
consumer projects. Test fixture text is explicitly treated as data in
`rust-testing`; N06 is its adversarial control.

## Per-skill disposition

| Skill | Disposition and reason |
| --- | --- |
| rust-implement | Targeted changes: behavior-sized work, meaningful baseline evidence, one check owner, explicit result boundaries; remove generic acronym advice |
| rust-testing | Targeted changes: defect-sensitive red/green evidence, fixture trust boundary, reuse by applicable inputs |
| rust-design | Targeted changes: grounded findings, contract violations versus heuristics, no invented findings |
| rust-debugging | Targeted changes: minimized reproducer, disconfirmation, recovery from ineffective fixes |
| rust-idiomatic | Retain caller contracts, borrowing/ownership, Arc sharing, safe operations and unsafe-invariant limits |
| rust-cli-interface | Retain parser/config precedence, explicit overrides, cheap help, terminal/data distinction |
| rust-errors | Retain partial success, typed causes, final cleanup, stream-specific BrokenPipe policy |
| rust-io | Retain bounded reads, byte fidelity, short operations, complete writes and observable flush |
| rust-filesystem | Retain identity, alias protection, race-aware creation, staged replacement and durability distinction |
| rust-processes | Retain literal arguments, bounded dual-stream draining, stdin EOF, status and process-tree ownership |
| rust-concurrency | Retain admission/queue/result bounds, cooperative cancellation and observed completion |
| rust-memory | Retain owner/retention analysis and the distinction between logical bounds and measured RSS |
| rust-performance | Retain separate workload metrics, comparable measurements and uncertainty without invented speedups |
| rust-cli-testing | Retain direct-parser versus process versus real-pipe/PTY evidence boundaries |
| rust-build | Retain targeted resolution inspection, lock integrity, MSRV and default-feature evidence |
| rust-distribution | Retain source/artifact compatibility and preparation versus publication authority |

Retaining a sound rule is a review outcome. Adding more prose to every skill would
not demonstrate improvement. Names, skill count, manifests, release version,
installation paths, and the single-file-per-skill contract remain unchanged.

## Bounded independent review, when supported

Use separate reviewers only for material independent questions. This is a
maintenance option, not a consumer workflow or prerequisite for a small edit.
Pin the base and candidate (or content hashes for an uncommitted patch), enumerate
the changed files once, and allocate coverage explicitly. Exclude generated files
only with a recorded reason; an uncovered file is not implicitly reviewed.

Give each reviewer the task, applicable contract, pinned diff, assigned files,
read-only tool permissions, and a time/tool-call budget. Spec/intent review asks
whether required behavior is missing or unauthorized scope was added. Technical
review asks whether Rust semantics, verification, or packaging contracts fail.
Keep initial reports isolated; reviewers do not see one another's conclusions.
A read-only prompt alone is not enforcement: the host must restrict write tools.

A material finding needs a location, violated contract, concrete failure mechanism,
supporting evidence, uncertainty, and the smallest repair. Recheck line positions
against the same candidate. Separate heuristics from defects and collapse duplicate
causes without concealing disagreement. Reviewers report examined and unexamined
scope, and do not rewrite files or repeat the owner's aggregate check suite.

The integrating owner adjudicates findings from evidence, not votes or a count of
agents. Repair accepted issues, rerun affected checks, and return changed areas to
the relevant reviewer only when needed. Stop when material findings are resolved
and assigned coverage and required checks are complete, or report the precise
remaining gap. Budget exhaustion, unavailable reviewers, and unfinished model
comparisons mean incomplete evidence, not a clean verdict. Do not keep adding
ritual rounds until somebody says "perfect".

## Evidence status for this authoring pass

The available session had no independent subagent runtime and no Cargo/rustc.
The author performed sequential source review and executed the new Python harness
tests; this is not independent multi-agent review. The Rust mutation check is
registered with existing Python discovery and explicitly skips without Cargo.
Remote CI results belong to the associated PR, not to an invented local run.
No model A/B trials, token savings, program speedups, or memory reductions are
claimed. The candidate is testable and reviewable, not empirically universal.
