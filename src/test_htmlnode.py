import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        # Test initialization with default parameters
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

        # Test initialization with all parameters
        children = [HTMLNode("p", "child")]
        props = {"class": "test-class", "id": "test-id"}
        node = HTMLNode("div", "content", children, props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "content")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_props_to_html_with_string_values(self):
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
        self.assertEqual(
            repr(node), "HTMLNode(tag=None, value=None, children=None, props=None)"
        )

        # Test string representation with complete node
        children = [HTMLNode("span", "child text")]
        props = {"class": "text-bold"}
        node = HTMLNode("p", "paragraph text", children, props)
        expected = (
            f"HTMLNode(tag=p, value=paragraph text, children={children}, props={props})"
        )
        self.assertEqual(repr(node), expected)

    def test_to_html(self):
        # Test that to_html raises NotImplementedError
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
