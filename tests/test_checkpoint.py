import datetime as dt
import json
import pathlib
import sys
import tempfile
import unittest
import urllib.error
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
        discovered = checkpoint.paper_identity(
            "https://unlisted-journal.org/papers/2602.00906",
            "Paper page - Hallucination is a Consequence of Space-Optimality",
        )
        self.assertEqual(abstract, discovered)

    def test_unlisted_public_hosts_are_candidates_but_private_hosts_are_not(self):
        self.assertIsNone(checkpoint.paper_identity("https://intranet.example/paper/secret.pdf", "Secret"))
        self.assertIsNone(checkpoint.paper_identity("http://arxiv.org/abs/2602.00906", "Paper"))
        self.assertIsNone(checkpoint.paper_identity("https://www.cis.upenn.edu/lecture-03.pdf", "Slides"))
        self.assertIsNone(checkpoint.paper_identity("https://public.example.net/Curriculum_Vitae.pdf", "Curriculum_Vitae.pdf"))
        self.assertIsNone(checkpoint.paper_identity("https://public.example.net/SurgeryInformationSheet.pdf", "SurgeryInformationSheet.pdf"))
        self.assertIsNone(checkpoint.paper_identity(
            "https://github.com/hanhan-mom/weekly-paper-tracker/blob/main/papers/example.md", "Own notes"
        ))
        candidate = checkpoint.paper_identity(
            "https://unlisted-journal.org/papers/novel-method.pdf?access_token=secret",
            "Novel Method",
        )
        self.assertEqual("https://unlisted-journal.org/papers/novel-method.pdf", candidate[2])
        self.assertIsNone(checkpoint.paper_identity(
            "https://unlisted-journal.org/papers/novel-method.pdf?token=secret",
            "PDF",
            {"https://unlisted-journal.org/papers/novel-method.pdf"},
        ))
        self.assertIsNotNone(checkpoint.paper_identity("https://example.com/private.pdf", "PDF"))

    def test_private_network_addresses_are_never_fetched(self):
        with patch.object(checkpoint.socket, "getaddrinfo", return_value=[
            (2, 1, 6, "", ("127.0.0.1", 443)),
        ]):
            with self.assertRaisesRegex(ValueError, "non-public network"):
                checkpoint.public_urlopen(checkpoint.urllib.request.Request(
                    "https://unlisted-journal.org/papers/novel-method.pdf"
                ))

    def test_credential_bearing_pdf_links_are_never_fetched(self):
        with self.assertRaisesRegex(ValueError, "credential-like query"):
            checkpoint.public_urlopen(checkpoint.urllib.request.Request(
                "https://unlisted-journal.org/paper.pdf?access_token=secret"
            ))

    def test_generic_public_html_paper_can_supply_pdf(self):
        paper = checkpoint.Paper("paper-test", "Research Paper",
                                 "https://unlisted-journal.org/content/opaque", dt.date(2026, 9, 21))
        page = checkpoint.PaperPage(paper.url)
        page.feed('<html><meta name="citation_pdf_url" content="/files/full-text.pdf"></html>')
        with patch.object(checkpoint, "public_page", return_value=page), \
             patch.object(checkpoint, "download_pdf", return_value="Introduction\nResults\nConclusion") as pdf:
            self.assertEqual("Introduction\nResults\nConclusion", checkpoint.paper_body(paper))
            pdf.assert_called_once_with("https://unlisted-journal.org/files/full-text.pdf")

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
        summary = {"is_research_paper": True, "summary_points": ["First point", "Second point"], "main_takeaway": "The takeaway"}
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

    def test_unverified_papers_stay_off_public_reports(self):
        paper = checkpoint.Paper("paper-123", "Unverified PDF",
                                 "https://unlisted-journal.org/paper/123.pdf", dt.date(2026, 9, 21))
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "papers").mkdir()
            (root / "weeks").mkdir()
            failure = urllib.error.HTTPError(paper.url, 403, "Forbidden", {}, None)
            with patch.object(checkpoint, "ROOT", root), \
                 patch.object(checkpoint, "papers_for_week", return_value=[paper]), \
                 patch.object(checkpoint, "summarize", side_effect=failure):
                self.assertTrue(checkpoint.checkpoint(dt.date(2026, 9, 21)))
                self.assertNotIn(paper.url, (root / "weeks/2026-09-21.md").read_text())
                queue = json.loads((root / ".review-queue/2026-09-21.json").read_text())
                self.assertEqual(paper.url, queue[0]["url"])

    def test_verified_unlisted_host_appears_in_weekly_report(self):
        paper = checkpoint.Paper("paper-public", "Novel Method",
                                 "https://unlisted-journal.org/files/novel-method.pdf", dt.date(2026, 9, 21))
        summary = {
            "is_research_paper": True,
            "summary_points": ["Method", "Finding"],
            "main_takeaway": "The method works in the reported setting.",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "papers").mkdir()
            (root / "weeks").mkdir()
            with patch.object(checkpoint, "ROOT", root), \
                 patch.object(checkpoint, "papers_for_week", return_value=[paper]), \
                 patch.object(checkpoint, "summarize", return_value=summary):
                self.assertFalse(checkpoint.checkpoint(dt.date(2026, 9, 21)))
            self.assertIn(paper.url, (root / "weeks/2026-09-21.md").read_text())
            self.assertTrue((root / "papers/paper-public.md").exists())


if __name__ == "__main__":
    unittest.main()
