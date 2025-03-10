from textnode import TextNode, TextType
import re

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
