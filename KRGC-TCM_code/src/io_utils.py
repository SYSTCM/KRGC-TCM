"""Shared input/output helpers for the KRGC-TCM release scripts."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


SUPPORTED_INPUTS = {".csv", ".tsv", ".txt", ".xlsx", ".xls"}


def read_table(path: str | Path, **kwargs: object) -> pd.DataFrame:
    """Read a CSV/TSV or Excel table based on its filename extension."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_INPUTS:
        raise ValueError(f"Unsupported input format: {path}")
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path, **kwargs)
    separator = "\t" if suffix == ".tsv" else ","
    return pd.read_csv(path, sep=separator, **kwargs)


def write_csv(frame: pd.DataFrame, path: str | Path) -> None:
    """Write UTF-8 CSV and create its parent directory when needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, encoding="utf-8")


def normalise_text(values: pd.Series) -> pd.Series:
    """Remove missing/blank values and normalise surrounding whitespace."""
    return values.astype("string").str.strip().replace({"": pd.NA, "<NA>": pd.NA})


def clean_edge_table(
    frame: pd.DataFrame, left_column: str, right_column: str, left_name: str, right_name: str
) -> pd.DataFrame:
    """Select, normalise, and deduplicate a two-column edge table."""
    missing = {left_column, right_column}.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    result = frame[[left_column, right_column]].rename(
        columns={left_column: left_name, right_column: right_name}
    )
    result[left_name] = normalise_text(result[left_name])
    result[right_name] = normalise_text(result[right_name])
    return result.dropna().drop_duplicates().sort_values([left_name, right_name]).reset_index(drop=True)
