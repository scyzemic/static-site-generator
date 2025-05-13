from .html_node import HTMLNode


class LeafNode(HTMLNode):
    """
    A class representing a leaf node in an HTML document.
    """

    def __init__(self, tag, value, props=None):
        """
        Initialize the LeafNode with a tag, attributes, and text.

        :param tag: A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        :param value: A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        :param props: A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (`<a>` tag) might have `{"href": "https://www.google.com"}`
        """
        super().__init__(tag, value, None, props)

    def to_html(self):
        props_string = self.props_to_html() if self.props is not None else ""

        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"
