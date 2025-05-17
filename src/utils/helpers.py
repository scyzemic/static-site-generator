import os
import shutil


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
