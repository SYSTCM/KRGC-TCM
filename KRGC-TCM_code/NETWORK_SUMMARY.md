# KRGC-TCM data summary

| Measure | Current released value | Evidence in release |
| --- | ---: | --- |
| Pre-screening herb labels | 6,018 | `all_herb_component_edges.csv` |
| Retained herbs and natural plant medicines | 5,701 | `retained_herbs.csv` |
| SMILES-deduplicated component records | 22,444 | `component_registry.csv` |
| Integrated herb-component data rows | 106,864 | `all_herb_component_edges.csv` |
| Physical rows in the source Excel relation table | 106,865 | 106,864 data rows plus one header row |
| Retained herb-component edges | 103,105 | `retained_herb_component_edges.csv` |

## Important reconciliation

The manuscript text states that 6,011 drugs were initially collected and that 106,865 herb-component relationships were obtained. The current source workbook retains 6,018 initial herb labels. Its relation table contains 106,864 data records, or 106,865 physical Excel rows including the header. The 5,701 retained herbs and 22,444 final component structures match exactly.

The seven-label difference in the pre-screening count cannot be resolved from the provided source directory. It should be reconciled against the version used to prepare the manuscript before public release.

The retained edge table contains 22,658 distinct component labels. The final registry contains 22,444 unique structures, associated with 22,392 distinct component labels. These were saved at different curation stages; the release does not silently map unmatched labels.
