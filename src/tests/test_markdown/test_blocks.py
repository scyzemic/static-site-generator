import unittest
from markdown.blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_line(self):
        # Test with a single line of text
        md = "Just a single line of text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single line of text"])

    def test_multiple_empty_lines(self):
        # Test with multiple empty lines between paragraphs
        md = """First paragraph

        Second paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_whitespace_only_lines(self):
        # Test with lines containing only whitespace
        md = """First paragraph


Second paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_headings(self):
        # Test with markdown headings
        md = """# Heading 1

## Heading 2

### Heading 3"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading 1", "## Heading 2", "### Heading 3"])

    def test_lists(self):
        # Test with ordered and unordered lists
        md = """Unordered list:

- Item 1
- Item 2
- Item 3

Ordered list:

1. First item
2. Second item
3. Third item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Unordered list:",
                "- Item 1\n- Item 2\n- Item 3",
                "Ordered list:",
                "1. First item\n2. Second item\n3. Third item",
            ],
        )

    def test_blockquotes(self):
        # Test with blockquotes
        md = """Here's a quote:

> This is a blockquote
> It spans multiple lines

Normal text again."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here's a quote:",
                "> This is a blockquote\n> It spans multiple lines",
                "Normal text again.",
            ],
        )

    def test_horizontal_rules(self):
        # Test with horizontal rules
        md = """Text before rule

---

Text after rule"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Text before rule", "---", "Text after rule"])

    def test_mixed_content(self):
        # Test with a mix of markdown elements
        md = """# Static Site Generator

This is a **simple** static site generator.

## Features

- Markdown parsing
- HTML generation
- CSS styling

```python
# Example usage
md = "# Hello World"
html = convert_markdown_to_html(md)
```

> Note: This project is in development."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Static Site Generator",
                "This is a **simple** static site generator.",
                "## Features",
                "- Markdown parsing\n- HTML generation\n- CSS styling",
                '```python\n# Example usage\nmd = "# Hello World"\nhtml = convert_markdown_to_html(md)\n```',
                "> Note: This project is in development.",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph_type(self):
        # Test regular paragraph text
        block = "This is a simple paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Test multi-line paragraph
        block = "This is a paragraph\nwith multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Test paragraph with special characters
        block = "Paragraph with *stars* and _underscores_ and `code`."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_type(self):
        # Test heading level 1
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        # Test heading level 2
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        # Test heading level 6
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        # Test invalid heading (no space after #)
        block = "#NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Test invalid heading (more than 6 #'s)
        block = "####### Too Many Hashtags"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_type(self):
        # Test code block
        block = "```\ndef hello():\n    print('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        # Test code block with language specified
        block = "```python\ndef hello():\n    print('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        # Test incomplete code block (missing closing backticks)
        block = "```\ndef hello():\n    print('Hello, world!')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Test incomplete code block (missing opening backticks)
        block = "def hello():\n    print('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_type(self):
        # Test simple quote
        block = "> This is a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        # Test multi-line quote
        block = "> This is a quote\n> with multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        # Test quote with nested formatting
        block = "> Quote with **bold** and _italic_ text."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        # Test invalid quote (no space after >)
        block = ">Invalid quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_type(self):
        # Test simple unordered list item
        block = "- List item 1"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        # Test unordered list item with nested formatting
        block = "- List item with **bold** text"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        # Test invalid unordered list (no space after -)
        block = "-Invalid list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Test invalid unordered list (different character)
        block = "* List item"  # using * instead of -
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_type(self):
        # Test simple ordered list item
        block = "1. List item 1"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        # Test ordered list item with nested formatting
        block = "1. List item with **bold** text"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        # Test invalid ordered list (no space after number)
        block = "1.Invalid list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Test invalid ordered list (different start number)
        block = "2. List item starting with 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_type_error(self):
        # Test with non-string input
        with self.assertRaises(TypeError):
            block_to_block_type(123)

        with self.assertRaises(TypeError):
            block_to_block_type(None)

        with self.assertRaises(TypeError):
            block_to_block_type(["List", "not", "string"])
