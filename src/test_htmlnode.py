import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
