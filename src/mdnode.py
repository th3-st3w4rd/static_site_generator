from textnode import TextNode, TextType
from htmlnode import HTMLNode
import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    text_name = re.findall(r"(?<=\!\[)(.*?)(?=\]\()",text)
    url = re.findall(r"(?<=\]\()(.*?)(?=\))",text)
    zippered = list(zip(text_name,url))
    return zippered

def extract_markdown_links(text):
    text_name = re.findall(r"(?<=\[)(.*?)(?=\]\()",text)
    url = re.findall(r"(?<=\]\()(.*?)(?=\))",text)
    zippered = list(zip(text_name,url))
    return zippered


def split_nodes_link(old_nodes):
    results = []
    
    for old_node in old_nodes:
        n_text = old_node.text
        
        if old_node.text_type != TextType.TEXT:
            results.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)
        if not links:
            results.append(old_node)
            continue

        current_text = old_node.text

        for link_text, url in links:
            md_link = f"[{link_text}]({url})" 
            parts = current_text.split(md_link, 1)
            before_text = parts[0]

            if before_text:
                results.append(TextNode(before_text, TextType.TEXT))
        
            results.append(TextNode(link_text, TextType.LINK, url))
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        if current_text:
            results.append(TextNode(current_text, TextType.TEXT))
    return results

def split_nodes_image(old_nodes):
    results = []
    
    for old_node in old_nodes:
        n_text = old_node.text
        
        if old_node.text_type != TextType.TEXT:
            results.append(old_node)
            continue
        
        links = extract_markdown_images(old_node.text)
        if not links:
            results.append(old_node)
            continue

        current_text = old_node.text

        for link_text, url in links:
            md_link = f"![{link_text}]({url})" 
            parts = current_text.split(md_link, 1)
            before_text = parts[0]

            if before_text:
                results.append(TextNode(before_text, TextType.TEXT))
        
            results.append(TextNode(link_text, TextType.IMAGE, url))
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        if current_text:
            results.append(TextNode(current_text, TextType.TEXT))
    return results

def text_to_text_nodes(text):
    return split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_link(split_nodes_image(text)), "`", TextType.CODE), "**", TextType.BOLD), "_", TextType.ITALIC)
    

def markdown_to_blocks(md):
    results = []
    blocked = md.split("\n\n")
    for block in blocked:
        results.append(block.strip())
    return results

def block_to_block_type(single_block):
    if single_block.startswith("#"):
        return BlockType.HEADING
    elif single_block.startswith("```") and single_block.endswith("```"):
        return BlockType.CODE
    elif single_block.startswith("> "):
        return BlockType.QUOTE
    elif single_block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif single_block.startswith(". "):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def text_node_to_html_nodes(text_nodes):
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def create_block_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        text_nodes = text_to_text_nodes(block)
        html_nodes = text_node_to_html_nodes(text_nodes)
        return HTMLNode("p", None, html_nodes)
    elif block_type == BlockType.HEADING:
        level = 0
        for char in block:
            if char == "#":
                level +=1
            else:
                break
        heading_text = block[level:].strip()
        text_nodes = text_to_text_nodes(heading_text)
        heading_nodes = text_node_to_html_nodes(text_nodes)
        return HTMLNode(f"h{level}", None, heading_nodes)
    
    elif block_type == BlockType.CODE:
        code_content = block[3:-3].strip()
        text_node = TextNode(code_content, TextType.TEXT)
        code_node = text_node_to_html_node(text_node)
        return HTMLNode("pre", None, [HTMLNode("code", None, [code_node])])

    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        quote_content = ""
        for line in lines:
            if line.startswith(">"):
                if line.startswith("> "):
                    line = line[2:]
                else:
                    line = line[1:]
            quote_content += line + "\n"
        quote_content = quote_content.strip()
        text_nodes = text_to_text_nodes(quote_content)
        quote_nodes = text_node_to_html_nodes(text_nodes)
        return HTMLNode("blockquote", None, quote_nodes)
    
    elif block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        list_items = []
        for line in lines:
            if line.startswith("- "):
                item_text = line[2:]
                text_nodes = text_to_text_nodes(item_text)
                item_nodes = text_node_to_html_nodes(text_nodes)
                list_items.append(HTMLNode("li", None, item_nodes))
        return HTMLNode("ul", None, list_items)

    elif block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        list_items = []
        for line in lines:
            dot_index = line.find(". ")
            if dot_index > 0:
                prefix = line[:dot_index]
                if prefix.isdigit():
                    item_text = line[dot_index+2:]
                    text_nodes = text_to_text_nodes(item_text)
                    item_nodes = text_node_to_html_nodes(text_nodes)
                    list_items.append(HTMLNode("li", None, item_nodes))
        return HTMLNode("ol", None, list_items)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children =[]
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = create_block_node(block, block_type)
        children.append(block_node)
    parent_node = HTMLNode("div", None, children)
    return parent_node

"""This is the psuedo imperitive testing"""
#test_string = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
#final = extract_markdown_images(test_string)
#print(final)

#test_string = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
#final = extract_markdown_links(test_string)
#print(final)

#test_node = TextNode("This is text with a `code block` word", TextType.TEXT)
#test_node = TextNode("This is text with a **bolded letters** word", TextType.TEXT)

#finals = split_nodes_delimeter([test_node], "**", TextType.BOLD)
#print(finals)

#node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
#final =  split_nodes_link([node])
#print(final)

#node = TextNode("This is text with an image ![Boot.dev Logo](https://www.boot.dev/img/bootdev-logo-full-small.webp) and ![Boot.dev Gem Bag](https://www.boot.dev/_nuxt/gems-glow-128.Bl75yAMH.webp) gem bag!",TextType.TEXT)
#final =  split_nodes_image([node])
#print(final)

#chacha = [TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)]
#final = text_to


#md = """
#This is **bolded** paragraph
#
#This is another paragraph with _italic_ text and `code` here
#This is the same paragraph on a new line
#
#- This is a list
#- with items
#"""
#final = markdown_to_blocks(md)
#print(final)

#test_md = """
# Title of things!

#This is **bolded** paragraph
#text in a p
#tag here

#This is another paragraph with _italic_ text and `code` here

#"""
#final = markdown_to_html_node(test_md)
#print(final)

