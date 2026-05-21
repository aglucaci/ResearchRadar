import datetime as dt
import unittest
import xml.etree.ElementTree as ET

from scripts.daily_pubmed_watch_v2 import _element_text, score_paper


class ScoringTests(unittest.TestCase):
    def test_pubmed_title_nested_taxon_text_is_preserved(self) -> None:
        node = ET.fromstring(
            "<ArticleTitle>Analysis of the genetic and phylogenetic context of "
            "<i>Escherichia coli</i> O77g:H18 associated with clustered cases "
            "of HUS in France in 2025</ArticleTitle>"
        )

        self.assertEqual(
            _element_text(node),
            "Analysis of the genetic and phylogenetic context of Escherichia coli "
            "O77g:H18 associated with clustered cases of HUS in France in 2025",
        )

    def test_cross_domain_research_signals_are_tagged_and_scored(self) -> None:
        result = score_paper(
            title="Immune escape and positive selection in viral genomic surveillance",
            abstract=(
                "We estimate dN/dS with codon models, reconstruct a phylogenetic tree, "
                "and analyze wastewater genomic surveillance during an outbreak."
            ),
            theme_key="Selection & codon models",
            published_date=dt.datetime.now(dt.timezone.utc),
            venue="Molecular Biology and Evolution",
        )

        self.assertGreater(result["score"], 10.0)
        self.assertIn("Selection", result["signal_classes"])
        self.assertIn("Viral evolution", result["signal_classes"])
        self.assertIn("Metagenomics / surveillance", result["signal_classes"])
        self.assertIn("research_signal", result["components"])
        self.assertGreater(result["components"]["cross_domain"], 0.0)


if __name__ == "__main__":
    unittest.main()
