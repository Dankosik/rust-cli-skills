# Rust CLI Skills

Small, independent skills for clean, idiomatic Rust command-line utilities, with an emphasis on fast execution and controlled memory use.

Each skill starts with a familiar engineering concept and directs a decision: what to inspect, how to reason, and what would make the result convincing. The model brings its Rust and ecosystem knowledge. Your project supplies the versions, conventions, and constraints.

One `SKILL.md` per skill. No reference libraries, setup ceremony, mandatory process, or dependencies between skills.

## Scope

This pack targets command-line tools: arguments and configuration, terminal and machine output, streaming data, filesystem operations, subprocesses, and executable distribution. It can support a future Rust CLI template; this repository contains the skills themselves.

The performance goal is explicit, but workload-specific. Startup latency, time to first result, throughput, peak memory, allocation rate, and binary size are separate properties. The skills favor bounded data flow and clear ownership, then require appropriate measurements for optimization claims. They do not prescribe an async runtime, unsafe code, a custom allocator, or one universal release profile.

## Install

Versioned release: [v1.0.0](https://github.com/Dankosik/rust-cli-skills/releases/tag/v1.0.0).
Install selected skills, or the entire pack, into your current project:

```sh
npx skills@1.5.25 add "Dankosik/rust-cli-skills#v1.0.0" --agent codex --skill '*' --copy
```

Use `--skill rust-implement` for one skill, or `--agent claude-code` for Claude
standalone placement. Node.js >=22.20.0 is required by this installer, not by
the skill instructions.

For native Claude Code and Codex installation, add the
[Dankosik marketplace](https://github.com/Dankosik/agent-skills-marketplace), then
install `rust-cli-skills@dankosik-skills`. The author catalog is available independently
of review for either provider's public directory.

[All installation methods, updates and rollback](docs/distribution.md) ·
[Versioning](docs/versioning.md) · [Changelog](CHANGELOG.md)

## Choose the decision

| Skill | Leading concept | Use it for |
| --- | --- | --- |
| [rust-implement](skills/rust-implement/SKILL.md) | Execution, Reuse, Clarity | Turn clear requirements into working Rust CLI code |
| [rust-idiomatic](skills/rust-idiomatic/SKILL.md) | Contracts | Ownership, borrowing, values, traits, and behavior-preserving cleanup |
| [rust-design](skills/rust-design/SKILL.md) | Cohesion | Responsibilities, modules, and abstractions that earn their cost |
| [rust-cli-interface](skills/rust-cli-interface/SKILL.md) | Composition | Arguments, configuration precedence, help, terminals, and output contracts |
| [rust-errors](skills/rust-errors/SKILL.md) | Failure semantics | Error context, diagnostics, exit status, partial success, and cleanup |
| [rust-io](skills/rust-io/SKILL.md) | Streaming | Bounded buffers, parsing, byte fidelity, backpressure, and output errors |
| [rust-filesystem](skills/rust-filesystem/SKILL.md) | File identity | Paths, traversal, temporary files, replacement, and data preservation |
| [rust-processes](skills/rust-processes/SKILL.md) | Process ownership | Child arguments, environment, pipes, termination, and reaping |
| [rust-concurrency](skills/rust-concurrency/SKILL.md) | Ownership | Threads, parallel work, async tasks, bounds, cancellation, and joining |
| [rust-memory](skills/rust-memory/SKILL.md) | Retention | Allocation, peak memory, collection capacity, and growing workloads |
| [rust-performance](skills/rust-performance/SKILL.md) | Evidence | Measured startup, runtime, throughput, CPU, and I/O improvements |
| [rust-debugging](skills/rust-debugging/SKILL.md) | Causality | Panics, wrong output, hangs, leaks, and platform-dependent failures |
| [rust-testing](skills/rust-testing/SKILL.md) | Behavior | Unit tests, I/O doubles, properties, fuzzing, and deterministic fixtures |
| [rust-cli-testing](skills/rust-cli-testing/SKILL.md) | Mechanism | Real binaries, exit status, streams, file effects, pipes, and terminals |
| [rust-build](skills/rust-build/SKILL.md) | Resolution | Cargo, toolchains, features, dependency resolution, and build profiles |
| [rust-distribution](skills/rust-distribution/SKILL.md) | Compatibility | Cargo packages, prebuilt binaries, installers, and supported targets |

Use `rust-implement` when the task is clear and the work is to implement it. Use a specialist when its particular decision needs attention. Each preserves supplied requirements and settled choices; none requires a design phase.

`rust-io` follows data through the pipeline; `rust-memory` accounts for what remains live; `rust-performance` measures whether a change helps the workload. `rust-testing` checks ordinary behavior; `rust-cli-testing` retains the actual process or OS mechanism. `rust-build` explains how the executable is produced; `rust-distribution` verifies how users receive and run it.

## Use

Ask naturally, or select a skill through your agent's explicit skill invocation:

- “Use rust-implement to implement this specification without changing its technical design.”
- “Use rust-cli-interface to add this subcommand while preserving machine-readable output.”
- “Use rust-io to process large input without retaining every record.”
- “Use rust-memory to find why memory grows with the number of files.”
- “Use rust-performance to compare startup and throughput of these two implementations.”
- “Use rust-processes to fix the hang when a child writes heavily to stderr.”
- “Use rust-cli-testing to verify broken-pipe behavior and the exit status.”

The pack preserves your Rust edition, minimum supported Rust version, target platforms, parser, runtime, and testing stack. Standard-library operations are the starting point for reuse; established crates remain valid choices when their semantics fit. Ordinary synchronous execution is sufficient for many commands. A runtime or specialized optimization should serve the utility's actual work.

Backend servers, GUI/TUI frameworks, embedded systems, and provider-specific deployment are outside the pack's primary scope. Filesystem, process, input, terminal, dependency, and unsafe-code risks are addressed where those decisions occur.

## Research basis

The selection and technical guidance were checked against primary Rust documentation and the maintainers' documentation for relevant tools:

- [The Rust Programming Language](https://doc.rust-lang.org/book/) and [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/checklist.html): ownership, representation, and caller contracts.
- [Command Line Applications in Rust](https://rust-cli.github.io/book/): CLI composition, output, tests, and distribution, with API details checked against current standard-library and crate documentation.
- [The Rust Performance Book](https://nnethercote.github.io/perf-book/): profiling, allocation, and build tradeoffs.
- [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html), [features](https://doc.rust-lang.org/cargo/reference/features.html), and [Rust version](https://doc.rust-lang.org/cargo/reference/rust-version.html): build and compatibility decisions.
- [std::io](https://doc.rust-lang.org/std/io/), [std::fs](https://doc.rust-lang.org/std/fs/), and [std::process](https://doc.rust-lang.org/std/process/): the actual boundaries behind streaming, files, and children.

These sources informed the instructions; skills do not require reading them to function. No single crate or build setting is claimed to be universally fastest.

## Contribute

Keep each skill independent and decision-focused. Prefer an established concept over a new glossary and a precise trigger over a capability catalog. Connect the promised property to a plausible failure, an observation that distinguishes it, and an appropriate completion criterion. Preserve meaningful differences through test fixtures and assertions.

Improve wording against a realistic task that exposed a weakness. Keep effort proportional to the change and keep API tutorials out of the skill. The pack uses the [Agent Skills format](https://agentskills.io/specification). Structural validity does not establish better model behavior or faster generated programs; those claims need separate evaluation.

## Acknowledgements

Follows the compact style of [Dankosik/golang-backend-skills](https://github.com/Dankosik/golang-backend-skills), [Dankosik/java-backend-skills](https://github.com/Dankosik/java-backend-skills), and [Dankosik/fastify-backend-skills](https://github.com/Dankosik/fastify-backend-skills). The instructions are written for Rust CLI semantics and work independently of those repositories.

[MIT license](LICENSE).
