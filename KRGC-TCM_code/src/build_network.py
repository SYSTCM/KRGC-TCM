"""Export the curated KRGC-TCM herb-component network as a standard graph."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from io_utils import clean_edge_table, read_table, write_csv


def make_node_id(node_type: str, label: str) -> str:
    return f"{node_type}:{label}"


def build_network(herb_components: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Return node, relationship, and lookup exports without inferring new edges."""
    herb_components = herb_components.drop_duplicates().copy()
    herb_component_lookup = (
        herb_components.groupby("herb", as_index=False)["compound"]
        .agg(lambda values: "、".join(sorted(set(values))))
        .rename(columns={"compound": "compounds"})
    )
    nodes = pd.concat(
        [
            pd.DataFrame(
                {
                    "node_id": herb_components["herb"].map(lambda value: make_node_id("herb", value)),
                    "node_type": "herb",
                    "label": herb_components["herb"],
                }
            ),
            pd.DataFrame(
                {
                    "node_id": herb_components["compound"].map(lambda value: make_node_id("compound", value)),
                    "node_type": "compound",
                    "label": herb_components["compound"],
                }
            ),
        ],
        ignore_index=True,
    ).drop_duplicates().sort_values(["node_type", "label"]).reset_index(drop=True)
    relationships = herb_components.assign(
        source_id=herb_components["herb"].map(lambda value: make_node_id("herb", value)),
        relation="CONTAINS_COMPOUND",
        target_id=herb_components["compound"].map(lambda value: make_node_id("compound", value)),
        evidence="curated KRGC-TCM herb-component relation",
    )[["source_id", "relation", "target_id", "evidence"]]
    return {
        "herb_component_edges": herb_components,
        "herb_component_lookup": herb_component_lookup,
        "nodes": nodes,
        "relationships": relationships,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export the curated KRGC-TCM herb-component graph.")
    parser.add_argument("--herb-component", required=True, help="CSV/TSV/Excel table containing direct herb-component edges")
    parser.add_argument("--output-dir", required=True, help="Directory for generated CSV files")
    parser.add_argument("--herb-column", default="herb")
    parser.add_argument("--compound-column", default="compound")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    herb_components = clean_edge_table(
        read_table(args.herb_component), args.herb_column, args.compound_column, "herb", "compound"
    )
    tables = build_network(herb_components)
    output_dir = Path(args.output_dir)
    for name, table in tables.items():
        write_csv(table, output_dir / f"{name}.csv")
    print(f"Created KRGC-TCM graph: {len(tables['nodes']):,} nodes, {len(tables['relationships']):,} relationships.")


if __name__ == "__main__":
    main()
