import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_init(self):
        # Test initialization with required parameters
        node = TextNode("Plain text", TextType.NORMAL)
        self.assertEqual(node.text, "Plain text")
        self.assertEqual(node.text_type, TextType.NORMAL)
        self.assertIsNone(node.url)

        # Test initialization with all parameters
        node_with_url = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node_with_url.text, "Link text")
        self.assertEqual(node_with_url.text_type, TextType.LINK)
        self.assertEqual(node_with_url.url, "https://example.com")

    def test_eq_with_url(self):
        # Test equality with URLs
        link1 = TextNode("Link", TextType.LINK, "https://example.com")
        link2 = TextNode("Link", TextType.LINK, "https://example.com")
        link3 = TextNode("Link", TextType.LINK, "https://different.com")

        self.assertEqual(link1, link2)
        self.assertNotEqual(link1, link3)

    def test_inequality(self):
        # Test inequality with different texts
        node1 = TextNode("Text one", TextType.NORMAL)
        node2 = TextNode("Text two", TextType.NORMAL)
        self.assertNotEqual(node1, node2)

        # Test inequality with different text types
        bold_node = TextNode("Same text", TextType.BOLD)
        italic_node = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(bold_node, italic_node)

        # Test inequality with same text and types but different URLs
        image1 = TextNode("Image", TextType.IMAGE, "img1.jpg")
        image2 = TextNode("Image", TextType.IMAGE, "img2.jpg")
        self.assertNotEqual(image1, image2)

    def test_repr(self):
        # Test string representation
        normal_node = TextNode("Normal text", TextType.NORMAL)
        self.assertEqual(repr(normal_node), "TextNode(Normal text, normal, None)")

        link_node = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(
            repr(link_node), "TextNode(Link text, link, https://example.com)"
        )


if __name__ == "__main__":
    unittest.main()
