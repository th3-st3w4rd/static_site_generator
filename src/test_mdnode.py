import unittest
from mdnode import (
        split_nodes_delimiter,
        extract_markdown_links,
        extract_markdown_images,
        split_nodes_link,
        split_nodes_image,
        text_to_text_nodes,
        markdown_to_blocks,
        BlockType,
        block_to_block_type,
)

from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimeter_bold(self):
        node = TextNode("This is text with a **bolded letters** word", TextType.TEXT)
        results = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(results), "[TextNode(This is text with a , text, None), TextNode(bolded letters, bold, None), TextNode( word, text, None)]")
    
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

class TestExtractFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        test_string = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        output = extract_markdown_images(test_string)
        self.assertEqual(str(output), "[('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]")


    def test_extract_markdown_images(self):
        test_string = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        output = extract_markdown_links(test_string)
        self.assertEqual(str(output), "[('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]")

    def test_split_nodes_image(self):
        node = TextNode("This is text with an image ![Boot.dev Logo](https://www.boot.dev/img/bootdev-logo-full-small.webp) and ![Boot.dev Gem Bag](https://www.boot.dev/_nuxt/gems-glow-128.Bl75yAMH.webp) gem bag!",TextType.TEXT)
        new_nodes =  split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("Boot.dev Logo", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp"),
                TextNode(" and ", TextType.TEXT),
                TextNode("Boot.dev Gem Bag", TextType.IMAGE, "https://www.boot.dev/_nuxt/gems-glow-128.Bl75yAMH.webp"),
                TextNode(" gem bag!", TextType.TEXT)
            ], new_nodes
        )

    def  test_split_nodes_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ], new_nodes
        )

    def test_test_to_text(self):
        node =[TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)]
        new_node = text_to_text_nodes(node)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], new_node
        )


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_mardown_to_blocks_header(self):
        block_heading = "# This is a heading."
        block_type = block_to_block_type(block_heading)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_mardown_to_blocks_quote(self):
        block_quote = "> This is a quote!"
        block_type = block_to_block_type(block_quote)
        self.assertEqual(block_type, BlockType.QUOTE)


    def test_mardown_to_blocks_code(self):
        block_code = "``` This is code!```"
        block_type = block_to_block_type(block_code)
        self.assertEqual(block_type, BlockType.CODE)

    def test_mardown_to_blocks_ul(self):
        block_ul = "- This is a quote!"
        block_type = block_to_block_type(block_ul)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_mardown_to_blocks_ol(self):
        block_ol = ". 1 This is an ordered list."
        block_type = block_to_block_type(block_ol)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_mardown_to_blocks_(self):
        block_paragraph= "This is a plain ole' paragraph."
        block_type = block_to_block_type(block_paragraph)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
