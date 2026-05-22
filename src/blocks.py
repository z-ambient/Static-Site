from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import split_node_delim, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType, text_node_to_html_node

class BlockTypes(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith("#"):
        return BlockTypes.HEADING
    if block.startswith(">"):
        return BlockTypes.QUOTE
    if block.startswith("- "):
        return BlockTypes.UNORDERED_LIST
    if block[0].isdigit() and block[1:3] == ". ":
        return BlockTypes.ORDERED_LIST
    if block.startswith("```") and block.endswith("```"):
        return BlockTypes.CODE
    
    return BlockTypes.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []

    for block in blocks:
        stripped_block = block.strip()

        if stripped_block == "":
            continue

        stripped_blocks.append(block.strip())

    return stripped_blocks

def heading_level(block):
    header_level = 0

    for char in block:
        if char == "#":
            header_level += 1
        else:
            break

    return header_level

def text_to_children(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_node_delim(nodes, "**", TextType.BOLD)
    nodes = split_node_delim(nodes, "_", TextType.ITALIC)
    nodes = split_node_delim(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    list_of_nodes = []

    for node in nodes:
        list_of_nodes.append(text_node_to_html_node(node))

    return list_of_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockTypes.HEADING:
            level = heading_level(block)
            text = block[level + 1:]
            html_nodes.append(ParentNode(f"h{level}", text_to_children(text)))
        
        elif block_type == BlockTypes.QUOTE:
            lines = block.split("\n")
            clean_lines = []

            for line in lines:
                clean_lines.append(line[2:])
            
            clean_text = "\n".join(clean_lines)
            html_nodes.append(ParentNode("blockquote", text_to_children(clean_text)))

        elif block_type == BlockTypes.ORDERED_LIST:
            items = block.split("\n")
            list_items = []
            for item in items:
                split_items = item.split(". ", 1)
                list_items.append(ParentNode("li", text_to_children(split_items[1])))

            html_nodes.append(ParentNode("ol", list_items))
        
        elif block_type == BlockTypes.UNORDERED_LIST:
            items = block.split("\n")
            list_items = []
            for item in items:
                split_items = item.split("- ", 1)
                list_items.append(ParentNode("li", text_to_children(split_items[1])))

            html_nodes.append(ParentNode("ul", list_items))

        elif block_type == BlockTypes.PARAGRAPH:
            clean_text = block.replace("\n", " ")
            html_nodes.append(ParentNode("p", text_to_children(clean_text)))

        elif block_type == BlockTypes.CODE:
            code_text = block[4:-3]

            html_nodes.append(ParentNode("pre", [LeafNode("code", code_text)]))


    return ParentNode("div", html_nodes)