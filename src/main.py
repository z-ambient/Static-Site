from textnode import TextType, TextNode

def main():
    text_node = TextNode(text="Some great text", text_type=TextType.BOLD, url="https://www.google.com")
    print(text_node)

main()