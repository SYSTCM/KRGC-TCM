"""Print the counts needed to audit a KRGC-TCM release package."""

from __future__ import annotations

import argparse
import json

from io_utils import read_table


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate key KRGC-TCM release counts.")
    parser.add_argument("--all-edges", required=True)
    parser.add_argument("--retained-herbs", required=True)
    parser.add_argument("--retained-edges", required=True)
    parser.add_argument("--component-registry", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    all_edges = read_table(args.all_edges)
    retained_herbs = read_table(args.retained_herbs)
    retained_edges = read_table(args.retained_edges)
    registry = read_table(args.component_registry)
    summary = {
        "all_herb_component_edge_rows": len(all_edges),
        "all_herbs": all_edges["herb"].nunique(),
        "retained_herbs": retained_herbs["herb"].nunique(),
        "retained_herb_component_edge_rows": len(retained_edges),
        "retained_herbs_with_edges": retained_edges["herb"].nunique(),
        "component_registry_rows": len(registry),
        "component_registry_unique_smiles": registry["smiles"].nunique(),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
