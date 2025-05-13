import unittest
from nodes.html_node import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        # Test initialization with default parameters
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

        # Test initialization with all parameters
        props = {"class": "test-class", "id": "test-id"}
        node = HTMLNode("div", "content", None, props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "content")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, props)

    def test_props_to_html(self):
        # Test with string attribute values
        props = {
            "class": "test-class",
            "id": "test-id",
            "data-test": "value",
            "priority": 3,
        }
        node = HTMLNode(props=props)
        html_props = node.props_to_html()

        # The order of attributes might vary, so we check for each attribute separately
        self.assertEqual(
            ' class="test-class" id="test-id" data-test="value" priority="3"',
            html_props,
        )

    def test_repr(self):
        # Test string representation with empty node
        node = HTMLNode()
        self.assertEqual(repr(node), "HTMLNode(None, None, None, None)")

        # Test string representation with complete node
        children = [HTMLNode("span", "child text")]
        props = {"class": "text-bold"}
        node = HTMLNode("p", None, children, props)
        expected = f"HTMLNode(p, None, {children}, {props})"
        self.assertEqual(repr(node), expected)

    def test_to_html(self):
        # Test that to_html raises NotImplementedError
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
