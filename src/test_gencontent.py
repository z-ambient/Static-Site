import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        markdown = """# This is the title
This is some content."""
        title = extract_title(markdown)
        self.assertEqual("This is the title", title)    