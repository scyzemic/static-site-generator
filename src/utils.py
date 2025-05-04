from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if (
            isinstance(node, TextNode)
            and node.text_type == TextType.TEXT
            and delimiter in node.text
        ):
            delimiter_count = 0
            for char in node.text:
                if char == delimiter:
                    delimiter_count += 1
            if delimiter_count % 2 != 0:
                raise Exception(
                    f"You have an uneven number of {delimiter} in your text: {node.text}"
                )

            parts = node.text.split(delimiter)
            for i in range(len(parts)):
                if i % 2 != 0:
                    new_nodes.append(TextNode(parts[i], text_type))
                else:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes
