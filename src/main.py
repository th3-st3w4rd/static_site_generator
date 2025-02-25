from textnode import TextNode

def main():
    test = TextNode(text="Thit is a text node",text_type="bold",url="https://boot.dev")
    #test_2 = TextNode(text="This is a text node",text_type="bold",url="https://boot.dev")
    #print(test == test_2i)
    print(repr(test))
    

if __name__ == "__main__":
    main()
