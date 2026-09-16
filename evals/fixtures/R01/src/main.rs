use std::io::{self, Write};
use std::process::ExitCode;

fn run() -> Result<(), String> {
    let mut args = std::env::args().skip(1);
    let lower = args.next().ok_or("missing lower bound")?;
    let upper = args.next().ok_or("missing upper bound")?;
    let lower: i64 = lower.parse().map_err(|_| "invalid lower bound")?;
    let upper: i64 = upper.parse().map_err(|_| "invalid upper bound")?;
    let values: Vec<i64> = args
        .map(|arg| arg.parse().map_err(|_| "invalid value".to_owned()))
        .collect::<Result<_, _>>()?;
    let selected = skill_fixture::select(&values, lower, upper).map_err(str::to_owned)?;
    let mut output = io::stdout().lock();
    for value in selected {
        writeln!(output, "{value}").map_err(|error| error.to_string())?;
    }
    output.flush().map_err(|error| error.to_string())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("{error}");
            ExitCode::from(2)
        }
    }
}
