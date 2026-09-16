use std::io::{self, Write};

#[derive(Default)]
struct ControlledWriter {
    bytes: Vec<u8>,
    flushes: usize,
    fail_flush: bool,
    fail_after: Option<usize>,
    zero_write: bool,
}

impl Write for ControlledWriter {
    fn write(&mut self, bytes: &[u8]) -> io::Result<usize> {
        if self.fail_after == Some(self.bytes.len()) {
            return Err(io::Error::new(io::ErrorKind::PermissionDenied, "write sentinel"));
        }
        let count = if self.zero_write { 0 } else { bytes.len().min(1) };
        self.bytes.extend_from_slice(&bytes[..count]);
        Ok(count)
    }
    fn flush(&mut self) -> io::Result<()> {
        self.flushes += 1;
        if self.fail_flush {
            Err(io::Error::new(io::ErrorKind::Other, "flush sentinel"))
        } else {
            Ok(())
        }
    }
}

fn main() {
    let mut late = ControlledWriter { fail_flush: true, ..Default::default() };
    let error = skill_fixture::finish_output(&mut late, b"done\n").unwrap_err();
    assert_eq!(error.kind(), io::ErrorKind::Other);
    assert_eq!(error.to_string(), "flush sentinel");
    assert_eq!(late.bytes, b"done\n");
    assert_eq!(late.flushes, 1);

    let mut successful = ControlledWriter::default();
    skill_fixture::finish_output(&mut successful, b"ok\n").unwrap();
    assert_eq!(successful.bytes, b"ok\n");
    assert_eq!(successful.flushes, 1);

    let mut empty = ControlledWriter { fail_flush: true, ..Default::default() };
    assert!(skill_fixture::finish_output(&mut empty, b"").is_err());
    assert_eq!(empty.flushes, 1);

    let mut partial = ControlledWriter { fail_after: Some(2), ..Default::default() };
    let error = skill_fixture::finish_output(&mut partial, b"payload").unwrap_err();
    assert_eq!(error.kind(), io::ErrorKind::PermissionDenied);
    assert_eq!(partial.bytes, b"pa");
    assert_eq!(partial.flushes, 0);

    let mut zero = ControlledWriter { zero_write: true, ..Default::default() };
    let error = skill_fixture::finish_output(&mut zero, b"payload").unwrap_err();
    assert_eq!(error.kind(), io::ErrorKind::WriteZero);
    assert_eq!(zero.flushes, 0);
    println!("R06:5 checks complete");
}
