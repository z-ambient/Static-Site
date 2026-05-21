

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []

    for block in blocks:
        stripped_block = block.strip()

        if stripped_block == "":
            continue

        stripped_blocks.append(block.strip())

    return stripped_blocks