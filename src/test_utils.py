import unittest
from textnode import TextNode, TextType
from utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    split_nodes_delimiter,
    text_to_textnodes,
)


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
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
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
        nodes = [TextNode("**Bold** text and more **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "Bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " text and more ")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, "bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, " text")
        self.assertEqual(result[3].text_type, TextType.TEXT)

    def test_no_delimiters(self):
        # Test text with no delimiters
        nodes = [TextNode("Plain text without delimiters", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Plain text without delimiters")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_adjacent_delimiters(self):
        # Test text with adjacent delimiter pairs
        nodes = [TextNode("This text has **bold****adjacent** markers", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "This text has ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "adjacent")
        self.assertEqual(result[2].text_type, TextType.BOLD)
        self.assertEqual(result[3].text, " markers")
        self.assertEqual(result[3].text_type, TextType.TEXT)

    def test_empty_delimited_text(self):
        # Test empty text between delimiters
        nodes = [TextNode("This has an **** empty bold section", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "This has an ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, " empty bold section")
        self.assertEqual(result[1].text_type, TextType.TEXT)

    def test_mixed_node_types(self):
        # Test with a mix of text nodes and other types
        text_node = TextNode("This is **bold** text", TextType.TEXT)
        bold_node = TextNode("Already bold", TextType.BOLD)
        nodes = [text_node, bold_node]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
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
        nodes = [TextNode("This text has **uneven delimiters", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertTrue("uneven number of **" in str(context.exception))

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
        nodes = [TextNode("**Bold text at the start and end**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Bold text at the start and end")
        self.assertEqual(result[0].text_type, TextType.BOLD)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        text = "Here are multiple images: ![first](https://example.com/first.jpg) and ![second](https://example.com/second.png)"
        matches = extract_markdown_images(text)
        expected = [
            ("first", "https://example.com/first.jpg"),
            ("second", "https://example.com/second.png"),
        ]
        self.assertListEqual(expected, matches)

    def test_empty_alt_text(self):
        text = "Image with empty alt text: ![](https://example.com/empty.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/empty.jpg")], matches)

    def test_special_characters(self):
        text = "Image with special chars: ![Image with spaces & symbols!](https://example.com/image-with-hyphens.jpg?size=large&format=png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                (
                    "Image with spaces & symbols!",
                    "https://example.com/image-with-hyphens.jpg?size=large&format=png",
                )
            ],
            matches,
        )

    def test_no_images(self):
        text = "This text has no images, only a regular [link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_adjacent_images(self):
        text = "Adjacent images:![first](https://example.com/1.jpg)![second](https://example.com/2.jpg)"
        matches = extract_markdown_images(text)
        expected = [
            ("first", "https://example.com/1.jpg"),
            ("second", "https://example.com/2.jpg"),
        ]
        self.assertListEqual(expected, matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_multiple_links(self):
        text = "Here are multiple links: [first](https://example.com/first) and [second](https://example.com/second)"
        matches = extract_markdown_links(text)
        expected = [
            ("first", "https://example.com/first"),
            ("second", "https://example.com/second"),
        ]
        self.assertListEqual(expected, matches)

    def test_empty_text(self):
        text = "Link with empty text: [](https://example.com/empty)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com/empty")], matches)

    def test_special_characters_in_links(self):
        text = "Link with special chars: [Link with spaces & symbols!](https://example.com/page?id=123&section=main#heading)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                (
                    "Link with spaces & symbols!",
                    "https://example.com/page?id=123&section=main#heading",
                )
            ],
            matches,
        )

    def test_no_links(self):
        text = "This text has no links, only a regular image ![image](https://example.com/image.jpg)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_adjacent_links(self):
        text = "Adjacent links:[first](https://example.com/1)[second](https://example.com/2)"
        matches = extract_markdown_links(text)
        expected = [
            ("first", "https://example.com/1"),
            ("second", "https://example.com/2"),
        ]
        self.assertListEqual(expected, matches)

    def test_email_links(self):
        text = "Email link: [Contact Us](mailto:example@example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Contact Us", "mailto:example@example.com")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_images(self):
        # Test with text that contains no images
        node = TextNode("This is plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is plain text with no images", TextType.TEXT)], new_nodes
        )

    def test_image_at_start(self):
        # Test with image at the start of the text
        node = TextNode(
            "![lead image](https://example.com/lead.jpg) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("lead image", TextType.IMAGE, "https://example.com/lead.jpg"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        # Test with image at the end of the text
        node = TextNode(
            "This is text followed by ![closing image](https://example.com/closing.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text followed by ", TextType.TEXT),
                TextNode(
                    "closing image", TextType.IMAGE, "https://example.com/closing.jpg"
                ),
            ],
            new_nodes,
        )

    def test_only_image(self):
        # Test with text that is only an image
        node = TextNode("![solo image](https://example.com/solo.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("solo image", TextType.IMAGE, "https://example.com/solo.jpg")],
            new_nodes,
        )

    def test_adjacent_images(self):
        # Test with adjacent images without text between them
        node = TextNode(
            "![first](https://example.com/first.jpg)![second](https://example.com/second.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://example.com/first.jpg"),
                TextNode("second", TextType.IMAGE, "https://example.com/second.jpg"),
            ],
            new_nodes,
        )

    def test_empty_alt_text(self):
        # Test with image that has empty alt text
        node = TextNode(
            "Image with empty alt text: ![](https://example.com/empty.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with empty alt text: ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://example.com/empty.jpg"),
            ],
            new_nodes,
        )

    def test_multiple_nodes(self):
        # Test with multiple input nodes, including non-TEXT types
        text_node = TextNode(
            "Text with ![image](https://example.com/pic.jpg)", TextType.TEXT
        )
        bold_node = TextNode("Bold text", TextType.BOLD)
        italic_node = TextNode(
            "Italic with ![embedded](https://example.com/embed.jpg)", TextType.TEXT
        )

        new_nodes = split_nodes_image([text_node, bold_node, italic_node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/pic.jpg"),
                TextNode("Bold text", TextType.BOLD),
                TextNode("Italic with ", TextType.TEXT),
                TextNode("embedded", TextType.IMAGE, "https://example.com/embed.jpg"),
            ],
            new_nodes,
        )

    def test_complex_url(self):
        # Test with complex URL containing query parameters
        node = TextNode(
            "Image with complex URL: ![complex](https://example.com/image.jpg?size=large&format=png#section)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with complex URL: ", TextType.TEXT),
                TextNode(
                    "complex",
                    TextType.IMAGE,
                    "https://example.com/image.jpg?size=large&format=png#section",
                ),
            ],
            new_nodes,
        )

    def test_special_characters_in_alt(self):
        # Test with special characters in alt text
        node = TextNode(
            "Special chars: ![Alt with & and * symbols!](https://example.com/special.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Special chars: ", TextType.TEXT),
                TextNode(
                    "Alt with & and * symbols!",
                    TextType.IMAGE,
                    "https://example.com/special.jpg",
                ),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://link.com) and another [second link](https://link2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://link.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://link2.com"),
            ],
            new_nodes,
        )

    def test_no_links(self):
        # Test with text that contains no links
        node = TextNode("This is plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is plain text with no links", TextType.TEXT)], new_nodes
        )

    def test_link_at_start(self):
        # Test with link at the start of the text
        node = TextNode(
            "[lead link](https://example.com/lead) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("lead link", TextType.LINK, "https://example.com/lead"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        # Test with link at the end of the text
        node = TextNode(
            "This is text followed by [closing link](https://example.com/closing)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text followed by ", TextType.TEXT),
                TextNode("closing link", TextType.LINK, "https://example.com/closing"),
            ],
            new_nodes,
        )

    def test_only_link(self):
        # Test with text that is only a link
        node = TextNode("[solo link](https://example.com/solo)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("solo link", TextType.LINK, "https://example.com/solo")],
            new_nodes,
        )

    def test_adjacent_links(self):
        # Test with adjacent links without text between them
        node = TextNode(
            "[first](https://example.com/first)[second](https://example.com/second)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://example.com/first"),
                TextNode("second", TextType.LINK, "https://example.com/second"),
            ],
            new_nodes,
        )

    def test_empty_link_text(self):
        # Test with link that has empty text
        node = TextNode(
            "Link with empty text: [](https://example.com/empty)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with empty text: ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com/empty"),
            ],
            new_nodes,
        )

    def test_multiple_nodes(self):
        # Test with multiple input nodes, including non-TEXT types
        text_node = TextNode(
            "Text with [link](https://example.com/page)", TextType.TEXT
        )
        bold_node = TextNode("Bold text", TextType.BOLD)
        italic_node = TextNode(
            "Italic with [embedded](https://example.com/embed)", TextType.TEXT
        )

        new_nodes = split_nodes_link([text_node, bold_node, italic_node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com/page"),
                TextNode("Bold text", TextType.BOLD),
                TextNode("Italic with ", TextType.TEXT),
                TextNode("embedded", TextType.LINK, "https://example.com/embed"),
            ],
            new_nodes,
        )

    def test_complex_url(self):
        # Test with complex URL containing query parameters
        node = TextNode(
            "Link with complex URL: [complex](https://example.com/page?id=123&section=main#fragment)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with complex URL: ", TextType.TEXT),
                TextNode(
                    "complex",
                    TextType.LINK,
                    "https://example.com/page?id=123&section=main#fragment",
                ),
            ],
            new_nodes,
        )

    def test_special_characters_in_text(self):
        # Test with special characters in link text
        node = TextNode(
            "Special chars: [Text with & and * symbols!](https://example.com/special)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Special chars: ", TextType.TEXT),
                TextNode(
                    "Text with & and * symbols!",
                    TextType.LINK,
                    "https://example.com/special",
                ),
            ],
            new_nodes,
        )

    def test_email_link(self):
        # Test with mailto link
        node = TextNode(
            "Contact us at [our email](mailto:example@example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Contact us at ", TextType.TEXT),
                TextNode("our email", TextType.LINK, "mailto:example@example.com"),
            ],
            new_nodes,
        )

    def test_not_affected_by_image_syntax(self):
        # Test that the function doesn't process image markdown
        node = TextNode(
            "This has a ![image](https://example.com/image.jpg) and a [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "This has a ![image](https://example.com/image.jpg) and a ",
                    TextType.TEXT,
                ),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_link_with_angle_brackets(self):
        # Test with angle brackets in URL
        node = TextNode(
            "Link with angle brackets: [API docs](https://example.com/api<version>)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with angle brackets: ", TextType.TEXT),
                TextNode("API docs", TextType.LINK, "https://example.com/api<version>"),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), len(new_nodes))
        for i in range(len(result)):
            self.assertEqual(result[i].text, new_nodes[i].text)
            self.assertEqual(result[i].text_type, new_nodes[i].text_type)
            self.assertEqual(result[i].url, new_nodes[i].url)

    def test_plain_text(self):
        # Test with plain text without any markdown
        text = "This is just plain text without any formatting"
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, text)
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[0].url, None)

    def test_bold_only(self):
        # Test with text containing only bold formatting
        text = "This has **bold** formatting"
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" formatting", TextType.TEXT),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)

    def test_italic_only(self):
        # Test with text containing only italic formatting
        text = "This has _italic_ formatting"
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" formatting", TextType.TEXT),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)

    def test_code_only(self):
        # Test with text containing only code formatting
        text = "This has `code` formatting"
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" formatting", TextType.TEXT),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)

    def test_link_only(self):
        # Test with text containing only links
        text = "This has a [link](https://example.com) in it"
        expected = [
            TextNode("This has a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in it", TextType.TEXT),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)

    def test_image_only(self):
        # Test with text containing only images
        text = "This has an ![image](https://example.com/image.jpg) in it"
        expected = [
            TextNode("This has an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" in it", TextType.TEXT),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
            self.assertEqual(result[i].url, expected[i].url)

    def test_multiple_same_format(self):
        # Test with multiple instances of the same format type
        text = "This has **multiple** instances of **bold** text"
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("multiple", TextType.BOLD),
            TextNode(" instances of ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)

    def test_nested_formats(self):
        # Test with formats that appear to be nested (Note: actual nesting isn't supported)
        text = "This has **bold with _italic_ inside** text"
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold with _italic_ inside", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)

    def test_empty_string(self):
        # Test with an empty string
        text = ""
        result = text_to_textnodes(text)
        self.assertEqual(len(result), 0)

    def test_only_delimiters(self):
        # Test with text that is only delimiters (invalid markdown)
        text = "**"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_all_formats_at_edges(self):
        # Test with all format types at the beginning and end of the text
        text = "**Bold start** middle text _italic end_"
        expected = [
            TextNode("Bold start", TextType.BOLD),
            TextNode(" middle text ", TextType.TEXT),
            TextNode("italic end", TextType.ITALIC),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)
