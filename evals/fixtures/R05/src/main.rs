use std::io::{self, Write};

fn main() -> io::Result<()> {
    let mut output = io::stdout().lock();
    skill_fixture::copy_bytes(io::stdin().lock(), &mut output)?;
    output.flush()
}
