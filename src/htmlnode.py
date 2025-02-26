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
        for item in self.props:
            listed_html.append(f'{item}="{self.props[item]}"')
        finished_html = " ".join(listed_html)
        return finished_html
