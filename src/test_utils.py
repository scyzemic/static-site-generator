import unittest
from textnode import TextNode, TextType
from utils import text_node_to_html_node, split_nodes_delimiter


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("print('Hello World')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello World')")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode(
            "Image description", TextType.IMAGE, "https://example.com/image.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/image.png", "alt": "Image description"},
        )

    def test_unknown_type(self):
        node = TextNode("Unknown type", "unknown_type")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertTrue("Unknown text type" in str(context.exception))


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_asterisk(self):
        # Test with asterisk delimiter for bold text
        nodes = [TextNode("This is *bold* text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_nodes_underscore(self):
        # Test with underscore delimiter for italic text
        nodes = [TextNode("This is _italic_ text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_nodes_backtick(self):
        # Test with backtick delimiter for code text
        nodes = [TextNode("This is `code` text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        # Test text with multiple delimiter pairs
        nodes = [TextNode("*Bold* text and more *bold* text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text and more ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "bold")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, " text")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_no_delimiters(self):
        # Test text with no delimiters
        nodes = [TextNode("Plain text without delimiters", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain text without delimiters")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_adjacent_delimiters(self):
        # Test text with adjacent delimiter pairs
        nodes = [TextNode("This text has *bold**adjacent* markers", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "This text has ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "adjacent")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, " markers")
        self.assertEqual(result[4].text_type, TextType.TEXT)

    def test_empty_delimited_text(self):
        # Test empty text between delimiters
        nodes = [TextNode("This has an ** empty bold section", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This has an ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " empty bold section")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_mixed_node_types(self):
        # Test with a mix of text nodes and other types
        text_node = TextNode("This is *bold* text", TextType.TEXT)
        bold_node = TextNode("Already bold", TextType.BOLD)
        nodes = [text_node, bold_node]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "Already bold")
        self.assertEqual(result[3].text_type, TextType.BOLD)

    def test_uneven_delimiters(self):
        # Test exception with uneven number of delimiters
        nodes = [TextNode("This text has *uneven delimiters", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertTrue("uneven number of *" in str(context.exception))

    def test_special_character_delimiter(self):
        # Test with a special character as delimiter
        nodes = [TextNode("This has a $special$ delimiter", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "$", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This has a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "special")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " delimiter")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_delimiter_at_start_and_end(self):
        # Test delimiters at the start and end of text
        nodes = [TextNode("*Bold text at the start and end*", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Bold text at the start and end")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "")
        self.assertEqual(result[2].text_type, TextType.TEXT)
