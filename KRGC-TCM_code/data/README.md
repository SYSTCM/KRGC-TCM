# KRGC-TCM data dictionary

## Curated network

| File | Rows | Meaning |
| --- | ---: | --- |
| `all_herb_component_edges.csv` | 106,864 | One integrated and normalized herb-component record before the retained-herb screen. |
| `retained_herbs.csv` | 5,701 | One manually retained herb or natural plant medicine name. |
| `retained_herb_component_edges.csv` | 103,105 | One direct component relation for a retained herb. |
| `component_registry.csv` | 22,444 | One final component structural record. `smiles` is unique for every row. |

`all_herb_component_edges.csv` has `herb` and `compound`. It is the integrated relation table in the curation master. The physical Excel sheet has 106,865 rows because row 1 is the column header.

`retained_herb_component_edges.csv` is expanded from the curated per-herb component lists after screening. It is the appropriate input for graph export of the final retained network.

`component_registry.csv` has `compound` and `smiles`. A component name can appear with more than one structure, so the registry is counted by unique SMILES records rather than unique text names.

The retained edge table has 22,658 unique component labels, whereas the registry has 22,392 unique labels across 22,444 structures. These are separate curation-stage snapshots. The release preserves both tables and does not create an unverified name-only mapping. Run `src/reconcile_component_labels.py` to export the unmatched-label lists for review.

## Source workbooks

| File | Purpose |
| --- | --- |
| `curation_master.xlsx` | Integrated HERB, HIT 2.0, and TCMBank herb-component curation, including the retained-herb columns and aggregated component lists. |
| `component_name_standardisation.xlsx` | Working record for component-name standardization and SMILES deduplication. |
| `final_component_registry.xlsx` | Final 22,444-row SMILES registry used to generate `component_registry.csv`. |

The files retain original Chinese headings where appropriate so the extraction steps can be audited against the study workbooks.
