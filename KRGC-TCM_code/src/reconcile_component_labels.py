"""Report label overlap between retained herb-component edges and the SMILES registry."""

from __future__ import annotations

import argparse

import pandas as pd

from io_utils import read_table, write_csv


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit component-name overlap across KRGC-TCM curation stages.")
    parser.add_argument("--retained-edges", required=True)
    parser.add_argument("--component-registry", required=True)
    parser.add_argument("--output-prefix", required=True, help="Prefix for unmatched-label CSV files")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    edges = read_table(args.retained_edges)
    registry = read_table(args.component_registry)
    edge_names = set(edges["compound"].dropna().astype(str).str.strip())
    registry_names = set(registry["compound"].dropna().astype(str).str.strip())
    edge_only = sorted(edge_names - registry_names)
    registry_only = sorted(registry_names - edge_names)
    write_csv(pd.DataFrame({"compound": edge_only}), f"{args.output_prefix}_edge_only.csv")
    write_csv(pd.DataFrame({"compound": registry_only}), f"{args.output_prefix}_registry_only.csv")
    print(
        f"Retained-edge labels: {len(edge_names):,}; registry labels: {len(registry_names):,}; "
        f"shared: {len(edge_names & registry_names):,}; edge-only: {len(edge_only):,}; "
        f"registry-only: {len(registry_only):,}."
    )


if __name__ == "__main__":
    main()
