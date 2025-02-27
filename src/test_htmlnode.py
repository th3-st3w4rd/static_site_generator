import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        prop = {"href":"https://www.google.com","target":"_blank"}
        html_1 = HTMLNode(props=prop)
        results = html_1.props_to_html()
        self.assertEqual(results, 'href="https://www.google.com" target="_blank"')

    def test_to_html(self):
        html_1 = HTMLNode()
        self.assertRaises(NotImplementedError, lambda:html_1.to_html())

    def test_repr(self):
        html_1 = HTMLNode("p","this is a paragraph")
        self.assertEqual(html_1.__repr__(), "HTMLNode(p, this is a paragraph, None, None)")

class TestLeafNode(unittest.TestCase):
    def test_value_error(self):
        leaf_1 = LeafNode("a",None,{"href":"https//:www.google.com"})
        self.assertRaises(ValueError, lambda: leaf_1.to_html())
    
    def test_tag_is_none(self):
        leaf_1 = LeafNode(None,"This is a paragraph", None)
        results = leaf_1.to_html()
        self.assertEqual(results, "This is a paragraph")
    
    def test_basic_leaf_node(self):
        leaf_1 = LeafNode("p","This is a paragraph", None)
        results = leaf_1.to_html()
        self.assertEqual(results,"<p>This is a paragraph</p>")
    
    def test_leaf_node_with_props(self):
        leaf_1 = LeafNode("a","Click Me!",{"href":"https://www.google.com"})
        self.assertEqual(leaf_1.to_html(),'<a href="https://www.google.com">Click Me!</a>')

class TestParentNode(unittest.TestCase):
    def test_basic_parent_node(self):
        results = ParentNode("p",[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),],)
        self.assertEqual(results.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_no_tag_error(self):
        results = ParentNode(None,[LeafNode("b", "Bold text"), LeafNode("i", "italic text")])
        self.assertRaises(ValueError, lambda: results.to_html())
    
    def test_no_child_error(self):
        results = ParentNode(tag="p", children=None)
        self.assertRaises(ValueError,results.to_html)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)


if __name__ == "__main__":
    unittest.main()
