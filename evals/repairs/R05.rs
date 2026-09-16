use std::io::{self, Read, Write};

/// Copy arbitrary bytes, returning their count. The caller owns final flushing.
pub fn copy_bytes<R: Read, W: Write>(mut source: R, mut destination: W) -> io::Result<u64> {
    io::copy(&mut source, &mut destination)
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
