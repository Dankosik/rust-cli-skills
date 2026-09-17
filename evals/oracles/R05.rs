use std::io::{self, Read, Write};

struct OneByte<R>(R);
impl<R: Read> Read for OneByte<R> {
    fn read(&mut self, buffer: &mut [u8]) -> io::Result<usize> {
        let length = buffer.len().min(1);
        self.0.read(&mut buffer[..length])
    }
}

#[derive(Default)]
struct ShortWriter(Vec<u8>);
impl Write for ShortWriter {
    fn write(&mut self, bytes: &[u8]) -> io::Result<usize> {
        let count = bytes.len().min(1);
        self.0.extend_from_slice(&bytes[..count]);
        Ok(count)
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

struct ReadFailure;
impl Read for ReadFailure {
    fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
        Err(io::Error::new(io::ErrorKind::PermissionDenied, "read sentinel"))
    }
}

struct WriteFailure;
impl Write for WriteFailure {
    fn write(&mut self, _: &[u8]) -> io::Result<usize> {
        Err(io::Error::new(io::ErrorKind::PermissionDenied, "write sentinel"))
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

struct ZeroWriter;
impl Write for ZeroWriter {
    fn write(&mut self, _: &[u8]) -> io::Result<usize> {
        Ok(0)
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

fn main() {
    let cases: &[&[u8]] = &[
        b"\xff\0\r\nx\nx\n\x80",
        b"a  \r\n",
        b"final record",
        b"",
        b"\r\n\n\r",
        b"same\nsame\n",
    ];
    for input in cases {
        let mut output = ShortWriter::default();
        let count = skill_fixture::copy_bytes(OneByte(*input), &mut output).unwrap();
        assert_eq!(output.0.as_slice(), *input, "raw bytes differ");
        assert_eq!(count, input.len() as u64, "byte count differs");
    }
    let error = skill_fixture::copy_bytes(ReadFailure, Vec::new()).unwrap_err();
    assert_eq!(error.kind(), io::ErrorKind::PermissionDenied);
    let error = skill_fixture::copy_bytes(&b"data"[..], WriteFailure).unwrap_err();
    assert_eq!(error.kind(), io::ErrorKind::PermissionDenied);
    let error = skill_fixture::copy_bytes(&b"data"[..], ZeroWriter).unwrap_err();
    assert_eq!(error.kind(), io::ErrorKind::WriteZero);
    println!("R05:9 checks complete");
}
