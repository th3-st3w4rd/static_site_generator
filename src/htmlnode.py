class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        listed_html = []
        copy_props = self.props.copy()
        for item in copy_props:
            listed_html.append(f'{item}="{copy_props[item]}"')
        finished_html = " ".join(listed_html)
        return finished_html

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return str(self.value)
        
        if self.props is not None:
            new_props = self.props_to_html()
            return f"<{self.tag} {new_props}>{self.value}</{self.tag}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("Yer missin' a 'tag'!")
        elif self.children is None:
            raise ValueError("There be no 'children' in this parameter!")
        else:
            results = list(map(lambda x: x.to_html(), self.children))
            results = "".join(results)
            final_html = f"<{self.tag}>{results}</{self.tag}>"
            return final_html










