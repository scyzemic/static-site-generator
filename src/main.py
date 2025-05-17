import sys
from utils.helpers import generate_pages_recursive, source_to_destination


def main():
    basepath = sys.argv[1] if sys.argv[1] else "/"

    source_to_destination("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
