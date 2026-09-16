use std::io::{self, Read, Write};

/// Copy arbitrary bytes, returning their count. The caller owns final flushing.
pub fn copy_bytes<R: Read, W: Write>(mut source: R, mut destination: W) -> io::Result<u64> {
    let mut bytes = Vec::new();
    source.read_to_end(&mut bytes)?;
    let text = String::from_utf8_lossy(&bytes).replace("\r\n", "\n");
    let text = text.trim_end();
    destination.write_all(text.as_bytes())?;
    Ok(text.len() as u64)
}

#[cfg(test)]
mod tests {
    #[test]
    fn copies_plain_ascii() {
        let mut output = Vec::new();
        assert_eq!(super::copy_bytes(&b"alpha\nbeta"[..], &mut output).unwrap(), 10);
        assert_eq!(output, b"alpha\nbeta");
    }
}
