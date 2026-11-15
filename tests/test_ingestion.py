import unittest

from ingestion.ingest import clean, safe_filename, split_chunks


class IngestionTests(unittest.TestCase):
    def test_clean_collapses_whitespace(self):
        self.assertEqual(clean("  RBI\\n  KYC   Directions "), "RBI KYC Directions")

    def test_split_chunks_preserves_content(self):
        text = " ".join(f"word{i}" for i in range(100))
        chunks = split_chunks(text, size=100, overlap=15)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(chunks))
        self.assertIn("word0", chunks[0])
        self.assertIn("word99", chunks[-1])

    def test_split_chunks_rejects_invalid_overlap(self):
        with self.assertRaises(ValueError):
            split_chunks("some text", size=10, overlap=10)

    def test_safe_filename_removes_path_characters(self):
        self.assertEqual(safe_filename("../bad id", "pdf"), "___bad_id.pdf")


if __name__ == "__main__":
    unittest.main()
