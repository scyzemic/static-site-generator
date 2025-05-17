import unittest
from nodes.text_node import TextNode, TextType
from markdown.converter import (
    list_block_to_children,
    text_node_to_html_node,
    markdown_to_html_node,
    text_to_children,
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


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_leafs(self):
        self.maxDiff = None
        md = """
# This is a heading

## This is a subheading

### This is a sub-subheading

This is a paragraph with [a link](https://example.com) and ![an image](https://example.com/image.png)

- This is a list item
- This is another list item
- This is a third list item

[This is a link](https://example.com)

![This is an image](https://example.com/image.png)

This is a regular paragraph.
_This is an italics block._

**This is bold text.** And regular text in one paragraph.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>This is a heading</h1><h2>This is a subheading</h2><h3>This is a sub-subheading</h3><p>This is a paragraph with <a href="https://example.com">a link</a> and <img src="https://example.com/image.png" alt="an image"></img></p><ul><li>This is a list item</li><li>This is another list item</li><li>This is a third list item</li></ul><p><a href="https://example.com">This is a link</a></p><p><img src="https://example.com/image.png" alt="This is an image"></img></p><p>This is a regular paragraph. <i>This is an italics block.</i></p><p><b>This is bold text.</b> And regular text in one paragraph.</p></div>',
        )


class TestTextToChildren(unittest.TestCase):
    def test_empty_string(self):
        """Test that an empty string produces an empty list of children."""
        children = text_to_children("")
        self.assertEqual(len(children), 0)

    def test_simple_text(self):
        """Test conversion of simple text without markdown formatting."""
        children = text_to_children("Simple text")
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].tag, None)
        self.assertEqual(children[0].value, "Simple text")

    def test_formatted_text(self):
        """Test conversion of text with various markdown formatting."""
        children = text_to_children("Text with **bold**, _italic_, and `code`")
        self.assertEqual(len(children), 6)
        # Text
        self.assertEqual(children[0].tag, None)
        self.assertEqual(children[0].value, "Text with ")
        # Bold
        self.assertEqual(children[1].tag, "b")
        self.assertEqual(children[1].value, "bold")
        # Text
        self.assertEqual(children[2].tag, None)
        self.assertEqual(children[2].value, ", ")
        # Italic
        self.assertEqual(children[3].tag, "i")
        self.assertEqual(children[3].value, "italic")
        # Text
        self.assertEqual(children[4].tag, None)
        self.assertEqual(children[4].value, ", and ")
        # Code
        self.assertEqual(children[5].tag, "code")
        self.assertEqual(children[5].value, "code")

    def test_with_link_and_image(self):
        """Test conversion of text with links and images."""
        children = text_to_children(
            "Text with [link](https://example.com) and ![image](https://example.com/img.jpg)"
        )
        self.assertEqual(len(children), 4)
        # Text
        self.assertEqual(children[0].tag, None)
        self.assertEqual(children[0].value, "Text with ")
        # Link
        self.assertEqual(children[1].tag, "a")
        self.assertEqual(children[1].value, "link")
        self.assertEqual(children[1].props, {"href": "https://example.com"})
        # Text
        self.assertEqual(children[2].tag, None)
        self.assertEqual(children[2].value, " and ")
        # Image
        self.assertEqual(children[3].tag, "img")
        self.assertEqual(children[3].value, "")
        self.assertEqual(
            children[3].props, {"src": "https://example.com/img.jpg", "alt": "image"}
        )


class TestListBlockToChildren(unittest.TestCase):
    def test_unordered_list(self):
        """Test conversion of an unordered list block."""
        block = "- Item 1\n- Item 2\n- Item 3"
        children = list_block_to_children(block, "ul")

        self.assertEqual(len(children), 3)

        # Check each list item
        for i, child in enumerate(children):
            self.assertEqual(child.tag, "li")
            self.assertEqual(len(child.children), 1)
            self.assertEqual(child.children[0].tag, None)
            self.assertEqual(child.children[0].value, f"Item {i + 1}")

    def test_ordered_list(self):
        """Test conversion of an ordered list block."""
        block = "1. First item\n2. Second item\n3. Third item"
        children = list_block_to_children(block, "ol")

        self.assertEqual(len(children), 3)

        expected_values = ["First item", "Second item", "Third item"]
        # Check each list item
        for i, child in enumerate(children):
            self.assertEqual(child.tag, "li")
            self.assertEqual(len(child.children), 1)
            self.assertEqual(child.children[0].tag, None)
            self.assertEqual(child.children[0].value, expected_values[i])

    def test_with_formatting(self):
        """Test list items with markdown formatting."""
        block = "- Item with **bold**\n- Item with _italic_\n- Item with `code`"
        children = list_block_to_children(block, "ul")

        self.assertEqual(len(children), 3)

        # First item (with bold)
        self.assertEqual(children[0].tag, "li")
        self.assertEqual(len(children[0].children), 2)
        self.assertEqual(children[0].children[0].tag, None)
        self.assertEqual(children[0].children[0].value, "Item with ")
        self.assertEqual(children[0].children[1].tag, "b")
        self.assertEqual(children[0].children[1].value, "bold")

        # Second item (with italic)
        self.assertEqual(children[1].tag, "li")
        self.assertEqual(len(children[1].children), 2)
        self.assertEqual(children[1].children[0].tag, None)
        self.assertEqual(children[1].children[0].value, "Item with ")
        self.assertEqual(children[1].children[1].tag, "i")
        self.assertEqual(children[1].children[1].value, "italic")

        # Third item (with code)
        self.assertEqual(children[2].tag, "li")
        self.assertEqual(len(children[2].children), 2)
        self.assertEqual(children[2].children[0].tag, None)
        self.assertEqual(children[2].children[0].value, "Item with ")
        self.assertEqual(children[2].children[1].tag, "code")
        self.assertEqual(children[2].children[1].value, "code")

    def test_empty_list(self):
        """Test handling of an empty list."""
        block = ""
        children = list_block_to_children(block, "ul")
        self.assertEqual(len(children), 0)


class TestMarkdownToHtmlNodeAdditional(unittest.TestCase):
    def test_empty_markdown(self):
        """Test conversion of empty markdown."""
        node = markdown_to_html_node("")
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_blockquote(self):
        """Test conversion of blockquote."""
        md = "> This is a blockquote\n> with multiple lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with multiple lines</blockquote></div>",
        )

    def test_nested_formatting(self):
        """Test handling of nested formatting (even though not properly supported)."""
        md = "This paragraph has **bold with _nested italic_** text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        # The parser doesn't actually support proper nesting, so the nested formatting is treated as literal
        self.assertEqual(
            html,
            "<div><p>This paragraph has <b>bold with _nested italic_</b> text</p></div>",
        )

    def test_multiple_headings(self):
        """Test conversion of multiple headings with different levels."""
        md = """# H1 Heading

## H2 Heading

### H3 Heading

#### H4 Heading

##### H5 Heading

###### H6 Heading"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>H1 Heading</h1><h2>H2 Heading</h2><h3>H3 Heading</h3><h4>H4 Heading</h4><h5>H5 Heading</h5><h6>H6 Heading</h6></div>",
        )

    def test_mixed_list_types(self):
        """Test conversion of mixed list types."""
        md = """- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Unordered item 1</li><li>Unordered item 2</li></ul><ol><li>Ordered item 1</li><li>Ordered item 2</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
