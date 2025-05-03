import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here", {"href": "https://www.example.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.example.com">Click here</a>'
        )

    def test_leaf_to_html_tagless(self):
        node = LeafNode(None, "Plain text content")
        self.assertEqual(node.to_html(), "Plain text content")
