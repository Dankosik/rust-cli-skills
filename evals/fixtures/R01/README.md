# Inclusive range command

`fixture-cli LOWER UPPER [VALUE ...]` accepts signed 64-bit decimal integers.
Print each selected value on its own LF-terminated line, in input order, including
duplicates and both endpoints. Equal bounds are valid. An empty selection is a
successful empty stdout. Reversed bounds return status 2, empty stdout, and
`invalid range` followed by LF on stderr. Keep the existing argument grammar,
diagnostics, synchronous execution, public API, and dependencies.

The repository uses `cargo fmt --check` and `cargo test --locked --offline`.
Implement the requested behavior and retain a focused regression test.
The declared Rust version is a constraint, not a claim that it was verified here.
