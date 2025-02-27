from textnode import TextNode, TextType

def split_nodes_delimeter(old_nodes, delimeter, text_type):
    results = []
    for old_node in old_nodes:
    #    print(old_node.text.lstrip(delimeter))
        split_list = old_node.text.split(delimeter)


test_node = [TextNode("This is text with a `code block` word", TextType.TEXT)]
split_nodes_delimeter(test_node, "`", TextType.CODE)

