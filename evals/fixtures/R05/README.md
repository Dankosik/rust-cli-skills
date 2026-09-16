# Byte-copy routine

`copy_bytes` copies arbitrary bytes from Read to Write and returns the byte count.
Preserve invalid UTF-8, NUL, CRLF, trailing whitespace, duplicate records, ordering,
and a final unterminated record exactly. Handle short reads/writes and propagate
read/write errors. Growing input must not require whole-input materialization.
The caller owns final flushing. Preserve the public API, execution model, and
std-only dependencies. The affected property can be tested through Read/Write;
no terminal or pipe behavior is claimed.

Existing checks: `cargo fmt --check`, `cargo test --locked --offline`.
Repair the defect and add focused regression coverage using independent bytes.
