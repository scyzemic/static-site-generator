import unittest
from nodes import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        child_node3 = LeafNode("span", "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span><span>child2</span><span>child3</span></div>",
        )

    def test_nested_parent_nodes(self):
        leaf1 = LeafNode("p", "text1")
        leaf2 = LeafNode("p", "text2")
        inner_parent1 = ParentNode("div", [leaf1])
        inner_parent2 = ParentNode("section", [leaf2])
        outer_parent = ParentNode("main", [inner_parent1, inner_parent2])
        self.assertEqual(
            outer_parent.to_html(),
            "<main><div><p>text1</p></div><section><p>text2</p></section></main>",
        )

    def test_deeply_nested_structure(self):
        leaf = LeafNode("span", "content")
        level3 = ParentNode("div", [leaf])
        level2 = ParentNode("section", [level3])
        level1 = ParentNode("article", [level2])
        root = ParentNode("main", [level1])
        self.assertEqual(
            root.to_html(),
            "<main><article><section><div><span>content</span></div></section></article></main>",
        )

    def test_with_props(self):
        child = LeafNode("span", "text", {"class": "highlight"})
        parent = ParentNode("div", [child], {"id": "container", "class": "wrapper"})
        self.assertEqual(
            parent.to_html(),
            '<div id="container" class="wrapper"><span class="highlight">text</span></div>',
        )

    def test_mixed_children_types(self):
        leaf1 = LeafNode("b", "bold")
        leaf2 = LeafNode("i", "italic")
        inner_parent = ParentNode("span", [leaf1])
        parent = ParentNode("div", [inner_parent, leaf2])
        self.assertEqual(
            parent.to_html(),
            "<div><span><b>bold</b></span><i>italic</i></div>",
        )

    def test_empty_children_list(self):
        # While the implementation might throw an error for no children,
        # an empty list of children is a valid edge case to test
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_none_children_error(self):
        with self.assertRaises(ValueError):
            parent = ParentNode("div", None)
            parent.to_html()

    def test_none_tag_error(self):
        with self.assertRaises(ValueError):
            parent = ParentNode(None, [LeafNode("p", "text")])
            parent.to_html()
