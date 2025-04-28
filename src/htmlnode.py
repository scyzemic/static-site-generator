class HTMLNode:
    """
    A class representing a node in an HTML document.
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Initialize the HTMLNode with a tag, attributes, and text.

        :param tag: A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        :param value: A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        :param children: A list of HTMLNode objects representing the children of this node.
        :param text: A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (`<a>` tag) might have `{"href": "https://www.google.com"}`
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def props_to_html(self):
        html_props = ""
        for key, value in self.props.items():
            html_props += f' {key}="{value}"'
        return html_props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
