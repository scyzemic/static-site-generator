import re
from nodes.text_node import TextNode, TextType


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    # We need to find [text](url) patterns that aren't preceded by an exclamation mark
    # Using a negative lookbehind (?<!) to ensure we don't match image syntax
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            # split the text into parts based on the image syntax so that we get [text, img, text, img, text, etc.]
            parts = re.split(r"(!\[.*?\]\(.*?\))", node.text)
            for part in parts:
                image_parts = extract_markdown_images(part)
                if len(image_parts) == 1:
                    image_node = TextNode(
                        image_parts[0][0], TextType.IMAGE, image_parts[0][1]
                    )
                    new_nodes.append(image_node)
                elif len(part) > 0:
                    text_node = TextNode(part, TextType.TEXT)
                    new_nodes.append(text_node)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            parts = re.split(r"((?<!!)\[.*?\]\(.*?\))", node.text)
            for part in parts:
                link_parts = extract_markdown_links(part)
                if len(link_parts) == 1:
                    link_node = TextNode(
                        link_parts[0][0], TextType.LINK, link_parts[0][1]
                    )
                    new_nodes.append(link_node)
                elif len(part) > 0:
                    text_node = TextNode(part, TextType.TEXT)
                    new_nodes.append(text_node)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if (
            isinstance(node, TextNode)
            and node.text_type == TextType.TEXT
            and delimiter in node.text
        ):
            matched = re.findall(re.escape(delimiter), node.text)
            if len(matched) % 2 != 0:
                raise Exception(
                    f"You have an uneven number of {delimiter} in your text: {node.text}"
                )

            parts = node.text.split(delimiter)
            for i in range(len(parts)):
                text = parts[i]
                if text == "":
                    continue
                if i % 2 != 0:
                    new_nodes.append(TextNode(parts[i], text_type))
                else:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes


def text_to_textnodes(text):
    links_processed_nodes = split_nodes_link([TextNode(text, TextType.TEXT)])
    images_processed_nodes = split_nodes_image(links_processed_nodes)
    bold_text_processed_nodes = split_nodes_delimiter(
        images_processed_nodes,
        "**",
        TextType.BOLD,
    )
    italic_text_processed_nodes = split_nodes_delimiter(
        bold_text_processed_nodes,
        "_",
        TextType.ITALIC,
    )
    code_text_processed_nodes = split_nodes_delimiter(
        italic_text_processed_nodes,
        "`",
        TextType.CODE,
    )

    return code_text_processed_nodes
