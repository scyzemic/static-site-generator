import re
from nodes.text_node import TextNode, TextType


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Extracts markdown image syntax from text.

    Args:
        text (str): The text to search for markdown image syntax.

    Returns:
        list: A list of tuples containing (alt_text, image_url) for each image found.
    """
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Extracts markdown link syntax from text, excluding image links.

    Args:
        text (str): The text to search for markdown link syntax.

    Returns:
        list: A list of tuples containing (link_text, url) for each link found.
    """
    # We need to find [text](url) patterns that aren't preceded by an exclamation mark
    # Using a negative lookbehind (?<!) to ensure we don't match image syntax
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Processes a list of TextNodes and converts image markdown syntax to image TextNodes.

    This function looks for image markdown syntax (![alt](url)) in text nodes and
    creates new image nodes, preserving the surrounding text as separate text nodes.

    Args:
        old_nodes (list): A list of TextNode objects to process.

    Returns:
        list: A new list of TextNodes with image markdown converted to image nodes.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
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


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Processes a list of TextNodes and converts link markdown syntax to link TextNodes.

    This function looks for link markdown syntax ([text](url)) in text nodes and
    creates new link nodes, preserving the surrounding text as separate text nodes.

    Args:
        old_nodes (list): A list of TextNode objects to process.

    Returns:
        list: A new list of TextNodes with link markdown converted to link nodes.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
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


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """
    Processes a list of TextNodes and converts delimited text to specified TextNode types.

    This function handles styled text like bold, italic, or code blocks by looking for
    paired delimiters (e.g., ** for bold, _ for italic) and converting the text between
    them to the appropriate TextNode type.

    Args:
        old_nodes (list): A list of TextNode objects to process.
        delimiter (str): The delimiter string that marks the styled text (e.g., "**", "_", "`").
        text_type (TextType): The TextType to apply to text between delimiters.

    Returns:
        list: A new list of TextNodes with delimited text converted to appropriate TextNode types.

    Raises:
        Exception: If there is an uneven number of delimiters in the text.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT and delimiter in node.text:
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


def text_to_text_nodes(text: str) -> list[TextNode]:
    """
    Converts raw markdown text to a list of TextNode objects.

    This function processes markdown text and transforms it into a structured list
    of TextNode objects representing different elements (links, images, bold text,
    italic text, code blocks, and plain text).

    The processing pipeline applies transformations in this order:
    1. Links
    2. Images
    3. Bold text (wrapped in **)
    4. Italic text (wrapped in _)
    5. Code text (wrapped in `)

    Args:
        text (str): The markdown text to convert.

    Returns:
        list: A list of TextNode objects representing the parsed markdown.
    """
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
