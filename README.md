# KRGC-TCM: curated herb-component knowledge network

This repository is the reproducibility release for the **KRGC-TCM** curated herb-component knowledge network. It contains the integrated HERB, HIT 2.0, and TCMBank curation workbooks, release-ready data tables, and Python scripts for extracting, validating, and exporting the network.

The primary network in this release is the direct **herb-component** graph. Downstream herb-target lookup tables and model-prediction matrices are intentionally excluded because they are not the database-curation layer described in the manuscript.

## Included contents

- `data/curated_network/`: standardized CSV files for the integrated herb-component data.
- `data/source_workbooks/`: the three source workbooks used for curation audit and reproducible extraction.
- `src/prepare_release_data.py`: extracts all release tables directly from the source workbooks.
- `src/build_network.py`: exports a standard node and relationship graph from a herb-component edge table.
- `src/validate_release.py`: prints key data counts for independent verification.
- `src/fetch_herb_data.py`: documented HERB API collection utility, retained for source-data provenance.
- `tests/`: a compact unit test for graph export behavior.

No model weights, clinical or patient data, API session cookies, or downstream target-prediction results are included.

## Released data

| File | Description |
| --- | --- |
| `all_herb_component_edges.csv` | Integrated, name-normalized herb-component records before herb screening. |
| `retained_herbs.csv` | The manually retained 5,701 traditional Chinese medicines and natural plant medicines. |
| `retained_herb_component_edges.csv` | Direct herb-component edges after applying the retained-herb list. |
| `component_registry.csv` | Final component registry, with 22,444 SMILES-deduplicated component records. |

See `data/README.md` and `NETWORK_SUMMARY.md` for field definitions, counts, and source-version reconciliation.

## Installation

Use Python 3.10 or later. From the repository root:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Recreate the release data

The following command recreates the CSV files from the included source workbooks:

```powershell
python src/prepare_release_data.py `
  --curation-master data/source_workbooks/curation_master.xlsx `
  --component-registry data/source_workbooks/final_component_registry.xlsx `
  --output-dir reproduced_data
```

## Export the retained knowledge graph

```powershell
python src/build_network.py `
  --herb-component data/curated_network/retained_herb_component_edges.csv `
  --output-dir results
```

The export writes four CSV files: `herb_component_edges.csv`, `herb_component_lookup.csv`, `nodes.csv`, and `relationships.csv`. Every relationship is a direct curated `CONTAINS_COMPOUND` edge. The script performs no target prediction or inferred-edge generation.

## Verify release counts

```powershell
python src/validate_release.py `
  --all-edges data/curated_network/all_herb_component_edges.csv `
  --retained-herbs data/curated_network/retained_herbs.csv `
  --retained-edges data/curated_network/retained_herb_component_edges.csv `
  --component-registry data/curated_network/component_registry.csv
```

## Source-data curation

The curation master records the integration of HERB, HIT 2.0, and TCMBank data, component-name standardization, and the manual exclusion of chemical drugs, Chinese medicine preparations, extracts, wild-animal medicines, and medicines not meeting the stated ethical criteria. The retained list contains 5,701 herb or natural plant medicine names.

The final component registry was built by standardizing component names and deduplicating structural representations using SMILES. It contains 22,444 rows with 22,444 unique SMILES values.

The retained herb-component edge table and the final SMILES registry are retained as separate curation-stage artifacts. The edge table has 22,658 distinct component labels; the registry has 22,392 distinct text labels across 22,444 structures. Use `src/reconcile_component_labels.py` to audit label overlap before making any new cross-stage mapping. The release does not impose an unverified name-only mapping.



## Suggested code-availability statement

> The KRGC-TCM curation code and knowledge network are provided as Supplementary Code/Data. The package contains the integrated herb-component source workbooks, the retained 5,701-herb list, the 22,444-component SMILES registry, standardized herb-component edge tables, and scripts for release-data extraction, network export, and validation.
