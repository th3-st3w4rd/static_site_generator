import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node_1 = TextNode("test node", TextType.ITALIC)
        node_2 = TextNode("test node", TextType.CODE)
        result = node_1 == node_2 
        self.assertFalse(result)

    def test_reper(self):
        node_1 = TextNode("test repr string", "links", "https://example.com")
        self.assertEqual(node_1.__repr__(), "TextNode(test repr string, links, https://example.com)")

if __name__ == "__main__":
    unittest.main()
