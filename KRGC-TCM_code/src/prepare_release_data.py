"""Extract reviewer-ready KRGC-TCM herb-component tables from source workbooks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from io_utils import clean_edge_table, normalise_text, read_table, write_csv


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare KRGC-TCM herb-component release data.")
    parser.add_argument("--curation-master", required=True, help="Integrated HERB/HIT 2.0/TCMBank workbook")
    parser.add_argument("--component-registry", required=True, help="Final SMILES-deduplicated component workbook")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--all-herb-column", default="Herb_cn_name.1")
    parser.add_argument("--all-compound-column", default="统一名称.1")
    parser.add_argument("--retained-herb-column", default="Herb_cn_name.3")
    parser.add_argument("--retained-aggregate-herb-column", default="Herb_cn_name.5")
    parser.add_argument("--retained-aggregate-compounds-column", default="Unnamed: 26")
    parser.add_argument("--registry-compound-column", default="成分名称")
    parser.add_argument("--registry-smiles-column", default="成分smiles")
    return parser.parse_args()


def expand_retained_components(master: pd.DataFrame, herb_column: str, compounds_column: str) -> pd.DataFrame:
    """Expand the curated Chinese-delimiter component lists into direct edges."""
    rows: list[tuple[str, str]] = []
    for herb, compounds in master[[herb_column, compounds_column]].dropna().itertuples(index=False, name=None):
        herb = str(herb).strip()
        if not herb:
            continue
        for compound in str(compounds).split("、"):
            compound = compound.strip()
            if compound:
                rows.append((herb, compound))
    return pd.DataFrame(rows, columns=["herb", "compound"]).drop_duplicates().sort_values(["herb", "compound"]).reset_index(drop=True)


def main() -> None:
    args = parse_arguments()
    master = read_table(args.curation_master)
    all_edges = clean_edge_table(
        master, args.all_herb_column, args.all_compound_column, "herb", "compound"
    )
    retained_herbs = normalise_text(master[args.retained_herb_column]).dropna().drop_duplicates().sort_values()
    retained_herbs = retained_herbs.rename("herb").reset_index(drop=True).to_frame()
    retained_edges = expand_retained_components(
        master, args.retained_aggregate_herb_column, args.retained_aggregate_compounds_column
    )

    registry_source = read_table(args.component_registry)
    component_registry = registry_source[[args.registry_compound_column, args.registry_smiles_column]].rename(
        columns={args.registry_compound_column: "compound", args.registry_smiles_column: "smiles"}
    )
    component_registry["compound"] = normalise_text(component_registry["compound"])
    component_registry["smiles"] = normalise_text(component_registry["smiles"])
    component_registry = component_registry.dropna().drop_duplicates().sort_values("smiles").reset_index(drop=True)

    output_dir = Path(args.output_dir)
    write_csv(all_edges, output_dir / "all_herb_component_edges.csv")
    write_csv(retained_herbs, output_dir / "retained_herbs.csv")
    write_csv(retained_edges, output_dir / "retained_herb_component_edges.csv")
    write_csv(component_registry, output_dir / "component_registry.csv")

    counts = {
        "all_herb_component_edge_rows": len(all_edges),
        "all_herbs": all_edges["herb"].nunique(),
        "all_normalised_compound_names": all_edges["compound"].nunique(),
        "retained_herbs": len(retained_herbs),
        "retained_herb_component_edge_rows": len(retained_edges),
        "retained_normalised_compound_names": retained_edges["compound"].nunique(),
        "component_registry_rows": len(component_registry),
        "component_registry_unique_smiles": component_registry["smiles"].nunique(),
    }
    (output_dir / "release_counts.json").write_text(json.dumps(counts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(counts, ensure_ascii=False))


if __name__ == "__main__":
    main()
