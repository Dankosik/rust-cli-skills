/// Select values in the inclusive range, preserving order and duplicates.
pub fn select(values: &[i64], lower: i64, upper: i64) -> Result<Vec<i64>, &'static str> {
    if lower > upper {
        return Err("invalid range");
    }
    Ok(values
        .iter()
        .copied()
        .filter(|value| lower <= *value && *value <= upper)
        .collect())
}

#[cfg(test)]
mod tests {
    use super::select;

    #[test]
    fn interior_values_keep_their_order() {
        assert_eq!(select(&[3, 1, 2, 1], 0, 4).unwrap(), [3, 1, 2, 1]);
    }

    #[test]
    fn reversed_range_is_invalid() {
        assert_eq!(select(&[], 2, 1), Err("invalid range"));
    }
}
