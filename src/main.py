import shutil
import os

def copy_static_to_public(src, dest):
    
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

def main():
    copy_static_to_public('static', 'public')

main()