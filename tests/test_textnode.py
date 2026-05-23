import unittest

from textnode import TextNode, TextType
from inline_markdown import split_node_delim

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_different_text(self):
        node = TextNode("This is sad text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_different(self):
        node = TextNode("text", TextType.BOLD, "youtube.com")
        node2 = TextNode("text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("text", TextType.BOLD)
        node2 = TextNode("text", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("text", TextType.CODE)
        node2 = TextNode("text", TextType.BOLD)
        self.assertNotEqual(node, node2)


class TestSplitNodeDelimiter(unittest.TestCase):

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_node_delim([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )
    
    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_node_delim([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )
        
    def test_split_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_node_delim([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_multiple_delimiters(self):
        node = TextNode("This has `code` and `more code`", TextType.TEXT)
        new_nodes = split_node_delim([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("more code", TextType.CODE),
            ],
        )


if __name__ == "__main__":
    unittest.main()