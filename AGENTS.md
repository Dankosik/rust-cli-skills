# Maintaining Rust CLI Skills

This repository authors independent instructions, not a Rust application.
Work directly on a clear request; a design document or agent team is not a prerequisite.

## Contracts

- Each installed skill remains self-contained: `SKILL.md` and `LICENSE` only.
  Keep authoring docs, evaluation fixtures, and orchestration outside `skills/`.
- Preserve skill names, installation paths, supported project choices, and the
  distinction between review, diagnosis, implementation, and publication.
- `plugin.json` owns metadata. Change it before synchronizing native manifests;
  do not hand-edit generated metadata or publish a release during instruction work.
- Improve a decision boundary against a concrete failure or counterexample.
  Keep Rust-specific invariants; remove generic advice that adds no decision.
  Descriptions select a decision, not every task touching Rust.

## Context and evidence

Use `docs/reference-review.md` when changing instruction behavior or coordinating
review. Use `docs/behavioral-evaluation.md` for the wider scenario protocol and
`evals/README.md` for executable fixtures. Use `docs/distribution.md` only for
packaging or installation changes. These are conditional pointers, not a reading list.

Select relevant checks from `.github/workflows/checks.yml`; one owner integrates
results. Reuse a passing result while its inputs, configuration, and environment
remain applicable. Workers do not repeat the owner's aggregate checks. Fix
introduced failures and rerun affected checks; unrelated failures remain distinct.
The new evaluator's unit tests join the existing Python test discovery; there is
no model call, paid service, or Rust toolchain installation in that fast gate.

Report packaging checks, fixture/oracle checks, and actual model evaluations
separately. A skipped toolchain, missing trace, exhausted review budget, or absent
subagent is unavailable evidence, not a pass. Never present serial self-review as
independent review. Keep releases and protected-branch integration owner-controlled.
