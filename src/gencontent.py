import os
from blocks import markdown_to_html_node



def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()      
    raise Exception("No title found in markdown content.")
        
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md_file = open(from_path, "r")
    md_content = md_file.read()

    template_file = open(template_path, "r")
    template_content = template_file.read()

    html_content = markdown_to_html_node(md_content).to_html()

    title = extract_title(md_content)

    final_content = template_content.replace("{{ Content }}", html_content)
    final_content = final_content.replace("{{ Title }}", title)
    final_content = final_content.replace('href="/', f'href="{basepath}')
    final_content = final_content.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_content)