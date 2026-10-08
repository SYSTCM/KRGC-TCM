"""Retrieve herb-compound or compound-target edges from the public HERB API.

The HERB endpoint and response schema can change. This acquisition script is
provided for provenance and re-collection; the release data are included in
data/curated_network and remain the analysis inputs for this study.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd
import requests

from io_utils import read_table, write_csv


API_URL = "http://herb.ac.cn/chedi/api/"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "KRGC-TCM research data collection (contact: replace-with-project-email)",
}


def request_detail(session: requests.Session, entity_type: str, entity_id: str) -> dict:
    payload = {"v": entity_id, "label": entity_type, "key_id": entity_id, "func_name": "detail_api"}
    response = session.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def parse_herb_ingredients(herb_id: str, payload: dict) -> list[dict[str, str]]:
    rows = []
    for item in payload.get("herb_ingredient", [])[1:]:
        if len(item) < 2 or not isinstance(item[0], dict):
            continue
        ingredient_id = str(item[0].get("title", "")).strip()
        ingredient_name = str(item[1]).strip()
        if ingredient_id and ingredient_name:
            rows.append({"herb_id": herb_id, "compound_id": ingredient_id, "compound": ingredient_name})
    return rows


def parse_compound_targets(compound_id: str, payload: dict) -> list[dict[str, str]]:
    rows = []
    for item in payload.get("ingredient_target", [])[1:]:
        if len(item) < 2 or not isinstance(item[0], dict):
            continue
        target_id = str(item[0].get("title", "")).strip()
        target_name = str(item[1]).strip()
        if target_id and target_name:
            rows.append({"compound_id": compound_id, "target_id": target_id, "target": target_name})
    return rows


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect HERB API relation data with incremental CSV output.")
    parser.add_argument("mode", choices=["herb-compounds", "compound-targets"])
    parser.add_argument("--input", required=True, help="CSV/TSV/Excel file containing IDs")
    parser.add_argument("--id-column", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--pause-seconds", type=float, default=0.5)
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    ids = read_table(args.input)[args.id_column].dropna().astype(str).str.strip().drop_duplicates()
    output = Path(args.output)
    existing = pd.read_csv(output) if output.exists() else pd.DataFrame()
    completed_ids = set(existing.iloc[:, 0].astype(str)) if not existing.empty else set()
    rows = existing.to_dict("records") if not existing.empty else []

    entity_type = "Herb" if args.mode == "herb-compounds" else "Ingredient"
    parser = parse_herb_ingredients if args.mode == "herb-compounds" else parse_compound_targets
    with requests.Session() as session:
        for index, entity_id in enumerate(ids, start=1):
            if entity_id in completed_ids:
                continue
            try:
                rows.extend(parser(entity_id, request_detail(session, entity_type, entity_id)))
            except requests.RequestException as error:
                print(f"Request failed for {entity_id}: {error}")
            if index % 50 == 0:
                write_csv(pd.DataFrame(rows), output)
            time.sleep(max(args.pause_seconds, 0))
    write_csv(pd.DataFrame(rows), output)
    print(f"Wrote {len(rows):,} retrieved relations to {output}.")


if __name__ == "__main__":
    main()
