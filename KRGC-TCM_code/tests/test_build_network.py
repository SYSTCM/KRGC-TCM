from pathlib import Path
import sys
import unittest

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from build_network import build_network  # noqa: E402


class BuildNetworkTest(unittest.TestCase):
    def test_graph_export_keeps_direct_curated_edges(self) -> None:
        edges = pd.DataFrame(
            {"herb": ["Herb_A", "Herb_A", "Herb_B", "Herb_A"], "compound": ["C1", "C2", "C1", "C1"]}
        )
        result = build_network(edges)

        self.assertEqual(len(result["herb_component_edges"]), 3)
        self.assertEqual(len(result["relationships"]), 3)
        self.assertEqual(len(result["nodes"]), 4)
        self.assertEqual(
            result["herb_component_lookup"].set_index("herb").loc["Herb_A", "compounds"], "C1、C2"
        )


if __name__ == "__main__":
    unittest.main()
