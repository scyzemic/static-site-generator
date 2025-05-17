import unittest

from src.utils.helpers import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Title\n\nThis is a test markdown file."
        expected_title = "Title"
        self.assertEqual(extract_title(markdown), expected_title)

    def test_extract_title_no_hash(self):
        markdown = "Title\n\nThis is a test markdown file."
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)
