import re
from nodes import LeafNode, TextType, TextNode, HTMLNode, ParentNode
from markdown.parser import text_to_text_nodes
from .blocks import BlockType, markdown_to_blocks, block_to_block_type


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown text type")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                content = block.split(" ")
                heading_level = content[0].count("#")
                text = " ".join(content[1:])
                children = text_to_children(text)
                node = ParentNode(f"h{heading_level}", children)
                html_nodes.append(node)
            case BlockType.PARAGRAPH:
                children = text_to_children(block)
                node = ParentNode("p", children)
                html_nodes.append(node)
            case BlockType.QUOTE:
                text = block.splitlines(True)
                text = [line[2:].strip() for line in text if line.strip()]
                children = text_to_children("\n".join(text))
                node = ParentNode("blockquote", children)
                html_nodes.append(node)
            case BlockType.UNORDERED_LIST:
                children = list_block_to_children(block, "ul")
                node = ParentNode("ul", children)
                html_nodes.append(node)
            case BlockType.ORDERED_LIST:
                children = list_block_to_children(block, "ol")
                node = ParentNode("ol", children)
                html_nodes.append(node)
            case BlockType.CODE:
                content = block.splitlines()
                text_node = TextNode("\n".join(content[1:-1]) + "\n", TextType.CODE)
                children = [text_node_to_html_node(text_node)]
                node = ParentNode("pre", children)
                html_nodes.append(node)
            case _:
                pass

    return ParentNode("div", html_nodes)


def text_to_children(text: str) -> list[HTMLNode]:
    """
    Convert a string of text to a list of HTML nodes.

    :param text: A string.
    :return: A list of HTML nodes.
    """

    text_nodes = text_to_text_nodes(" ".join(text.split("\n")))
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def list_block_to_children(block: str, type: str) -> list[HTMLNode]:
    """
    Convert a list block to a list of HTML nodes.

    :param block: A string representing a list block.
    :param type: The type of list ("ul" or "ol").
    :return: A list of HTML nodes.
    """
    children = []
    regex = r"^\-\s" if type == "ul" else r"^\d.\s"
    trim_amount = 2 if type == "ul" else 3
    items = block.split("\n")
    for item in items:
        if item.strip():
            item_content = (
                item.strip()[trim_amount:]
                if re.match(regex, item.strip())
                else item.strip()
            )
            children.append(ParentNode("li", text_to_children(item_content)))
    return children
