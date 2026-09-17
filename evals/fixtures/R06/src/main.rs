use std::io;

fn main() -> io::Result<()> {
    skill_fixture::finish_output(&mut io::stdout().lock(), b"done\n")
}
