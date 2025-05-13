from .html_node import HTMLNode


class ParentNode(HTMLNode):
    """
    A class representing a parent node in an HTML document.
    """

    def __init__(self, tag, children, props=None):
        """
        Initialize the ParentNode with a tag, attributes, and children.

        :param tag: A string representing the HTML tag name (e.g. "div", "span", etc.)
        :param children: A list of child nodes (which can be either LeafNode or ParentNode instances)
        :param props: A dictionary of key-value pairs representing the attributes of the HTML tag.
                      For example, a div might have {"class": "container", "id": "main"}
        """
        super().__init__(tag, None, children, props)

    def to_html(self):
        props_string = self.props_to_html() if self.props is not None else ""

        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if self.children is None:
            raise ValueError("ParentNode must have children.")

        children = "".join(child.to_html() for child in self.children)

        return f"<{self.tag}{props_string}>{children}</{self.tag}>"
