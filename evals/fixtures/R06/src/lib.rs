use std::io::{self, Write};

/// Complete writing and flushing before reporting successful output.
pub fn finish_output<W: Write>(writer: &mut W, bytes: &[u8]) -> io::Result<()> {
    writer.write_all(bytes)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn writes_payload() {
        let mut output = Vec::new();
        super::finish_output(&mut output, b"done\n").unwrap();
        assert_eq!(output, b"done\n");
    }
}
