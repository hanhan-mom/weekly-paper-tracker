import datetime as dt
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
import checkpoint


class PaperTrackerTests(unittest.TestCase):
    def test_paper_identity_deduplicates_abstract_and_pdf(self):
        abstract = checkpoint.paper_identity(
            "https://arxiv.org/abs/2602.00906",
            "[2602.00906] Hallucination is a Consequence of Space-Optimality",
        )
        pdf = checkpoint.paper_identity(
            "chrome-extension://reader/https://arxiv.org/pdf/2602.00906",
            "2602.00906v7.pdf",
        )
        self.assertEqual(abstract[0], pdf[0])
        self.assertEqual(abstract[2], pdf[2])
        self.assertEqual("Hallucination is a Consequence of Space-Optimality", abstract[1])

    def test_public_sources_only_and_tracking_query_removed(self):
        self.assertIsNone(checkpoint.paper_identity("https://intranet.example/paper/secret.pdf", "Secret"))
        self.assertIsNone(checkpoint.paper_identity("https://github.com/private-org/private-repo/blob/main/private.pdf", "Private"))
        self.assertIsNone(checkpoint.paper_identity("http://arxiv.org/abs/2602.00906", "Paper"))
        self.assertIsNone(checkpoint.paper_identity("https://www.cis.upenn.edu/lecture-03.pdf", "Slides"))
        private_url = "https://example.com/private.pdf"
        self.assertIsNone(checkpoint.paper_identity(
            "https://r.jordan.im/download/investing/example.pdf?token=secret",
            "PDF",
            {"https://r.jordan.im/download/investing/example.pdf"},
        ))
        self.assertIsNone(checkpoint.paper_identity(private_url, "PDF"))

    def test_excerpt_uses_main_body_and_conclusion(self):
        text = "Abstract\nBrief.\n1 Introduction\n" + ("Background. " * 1800)
        text += "\n2 Results\nMeasured gains.\n3 Conclusion\nThe central finding.\n"
        result = checkpoint.excerpt(text)
        self.assertIn("Measured gains", result)
        self.assertIn("The central finding", result)

    def test_poster_with_verified_arxiv_copy_uses_full_text(self):
        paper = checkpoint.Paper("neurips-115123", "Beyond the 80/20 Rule",
                                 "https://neurips.cc/virtual/2025/poster/115123", dt.date(2026, 9, 20))
        self.assertEqual("https://arxiv.org/pdf/2506.01939", checkpoint.pdf_url(paper))

    def test_exclusions_are_required_and_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            excluded = pathlib.Path(directory) / ".excluded-urls"
            with patch.object(checkpoint, "EXCLUDED_URLS_FILE", excluded):
                with self.assertRaises(FileNotFoundError):
                    checkpoint.load_excluded_urls()
                excluded.write_text("https://arxiv.org/abs/2602.00906\n")
                self.assertEqual({"https://arxiv.org/abs/2602.00906"},
                                 checkpoint.load_excluded_urls())
                excluded.write_text("https://arxiv.org/abs/2602.00906?token=private\n")
                with self.assertRaises(ValueError):
                    checkpoint.load_excluded_urls()

    def test_checkpoint_preserves_read_checkboxes_and_notes(self):
        paper = checkpoint.Paper("arxiv-2602-00906", "Rate-Distortion Paper",
                                 "https://arxiv.org/abs/2602.00906", dt.date(2026, 9, 21))
        summary = {"summary_points": ["First point", "Second point"], "main_takeaway": "The takeaway"}
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "papers").mkdir()
            (root / "weeks").mkdir()
            with patch.object(checkpoint, "ROOT", root), \
                 patch.object(checkpoint, "papers_for_week", return_value=[paper]), \
                 patch.object(checkpoint, "summarize", return_value=summary) as summarize:
                self.assertFalse(checkpoint.checkpoint(dt.date(2026, 9, 21)))
                report = root / "weeks/2026-09-21.md"
                report.write_text(report.read_text().replace("- [ ]", "- [x]"))
                note = root / "papers/arxiv-2602-00906.md"
                note.write_text(note.read_text() + "Personal observation\n")
                self.assertFalse(checkpoint.checkpoint(dt.date(2026, 9, 21)))
                self.assertIn("- [x]", report.read_text())
                self.assertIn("Personal observation", note.read_text())
                summarize.assert_called_once()


if __name__ == "__main__":
    unittest.main()
