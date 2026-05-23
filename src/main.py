import shutil
import os
import sys

from gencontent import generate_page

dir_path_content = "./content"
dir_path_templates = "./template.html"

def copy_static_to_docs(src, dest):
    
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.makedirs(dest)

    copy_directory(src, dest)

def copy_directory(src, dest):
    for item in os.listdir(src):
        source_path = os.path.join(src, item)
        destination_path = os.path.join(dest, item)

        if os.path.isdir(source_path):
            print(f"Copying directory: {source_path} to {destination_path}")
            os.makedirs(destination_path)

            copy_directory(source_path, destination_path)
        else:
            print(f"Copying file: {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)

def generate_pages_recursively(dest_path, template_path, current_dir, basepath):
    for item in os.listdir(current_dir):
        source_path = os.path.join(current_dir, item)
        destination_path = os.path.join(dest_path, item)

        if os.path.isdir(source_path):
            generate_pages_recursively(destination_path, template_path, source_path, basepath)
        elif item.endswith(".md"):
            html_path = os.path.join(dest_path, item.replace(".md", ".html"))
            generate_page(source_path, template_path, html_path, basepath)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static_to_docs('static', 'docs')
    generate_pages_recursively('docs', dir_path_templates, dir_path_content, basepath)

main()
