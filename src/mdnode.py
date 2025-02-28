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


#test_string = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
#final = extract_markdown_images(test_string)
#print(final)

test_string = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
final = extract_markdown_links(test_string)
print(final)

#test_node = TextNode("This is text with a `code block` word", TextType.TEXT)
#test_node = TextNode("This is text with a **bolded letters** word", TextType.TEXT)

#finals = split_nodes_delimeter([test_node], "**", TextType.BOLD)
#print(finals)

