import unittest

from blocks import markdown_to_blocks, block_to_block_type, BlockTypes, markdown_to_html_node

class TestSplitBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks_empty(self):
        md = """
        
        
        """
        
        blocks = markdown_to_blocks(md)

        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n  \n   "
        
        blocks = markdown_to_blocks(md)

        self.assertEqual(blocks, [])

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockTypes.HEADING)
        self.assertEqual(block_to_block_type("> Quote"), BlockTypes.QUOTE)
        self.assertEqual(block_to_block_type("- List item"), BlockTypes.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. List item"), BlockTypes.ORDERED_LIST)
        self.assertEqual(block_to_block_type("```code```"), BlockTypes.CODE)
        self.assertEqual(block_to_block_type("Paragraph"), BlockTypes.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )
    
    def test_ordered_list(self):
        md = """
1. Item 1
2. Item 2
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )
    
    def test_quote(self):
        md = """> This is a quote
> that spans multiple lines
> and should be in a blockquote tag
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nthat spans multiple lines\nand should be in a blockquote tag</blockquote></div>",
        )
    
    def test_heading(self):
        md = """
# Heading 1
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1></div>",
        )  