# Fallible output completion

`finish_output` must fully write the supplied bytes, then explicitly flush before
returning success. Flush even for an empty payload. Propagate the original write
or flush error; after a write error, return that error without attempting flush.
Keep the public API, synchronous execution, and std-only dependencies.
A controlled Write implementation is enough for this function-level contract;
these tests do not prove a real pipe or the executable's exit status.

Existing checks: `cargo fmt --check`, `cargo test --locked --offline`.
Fix the false-success path and retain a regression that exposes a late failure.
