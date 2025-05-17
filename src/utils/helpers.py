import os
import shutil

from markdown.converter import markdown_to_html_node


def source_to_destination(src: str, dest: str) -> None:
    """copies all content from the source directory to the destination directory recursively.
    This function will delete all the content in the destination directory before copying.

    Args:
        src (str): path to the source directory
        dest (str): path to the destination directory

    Returns:
        None
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory {src} does not exist.")

    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.makedirs(dest)

    for item in os.listdir(src):
        name = os.path.join(src, item)
        if os.path.isfile(name):
            print(f"Copying file {name} to {dest}/{item}")
            shutil.copy(name, dest)
        else:
            source_to_destination(name, os.path.join(dest, item))


def extract_title(markdown: str) -> str:
    """Extracts the title from a markdown file.

    Args:
        markdown (str): content of a markdown document

    Returns:
        str: title of the markdown file
    """
    title_line = markdown.split("\n")[0]
    if title_line.startswith("# "):
        return title_line[2:].strip()
    else:
        raise ValueError("Title not found in markdown file.")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """Given the path to a markdown file, a template file, and a destination path, parse the markdown file, convert it to HTML string, and generate a new HTML file using the template.

    Args:
        from_path (str): path to the markdown file
        template_path (str): path to the template file
        dest_path (str): path to the destination HTML file
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        file_contents = f.read()
        with open(template_path, "r") as t:
            template_contents = t.read()

            file_contents_html = markdown_to_html_node(file_contents).to_html()
            page_title = extract_title(file_contents)

            template_contents = template_contents.replace("{{ Title }}", page_title)
            template_contents = template_contents.replace(
                "{{ Content }}", file_contents_html
            )

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            with open(dest_path, "w") as f:
                f.write(template_contents)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    """Crawls the content directory and generates HTML pages to the public directory for each markdown file found using the template provided.

    Args:
        dir_path_content (str): _description_
        template_path (str): _description_
        dest_dir_path (str): _description_
    """
    for content in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, content)
        if os.path.isfile(content_path):
            if content.endswith(".md"):
                dest_path = os.path.join(dest_dir_path, content.replace(".md", ".html"))
                generate_page(content_path, template_path, dest_path)
        else:
            new_dest_dir = os.path.join(dest_dir_path, content)
            generate_pages_recursive(content_path, template_path, new_dest_dir)
