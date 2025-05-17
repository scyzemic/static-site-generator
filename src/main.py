from utils.helpers import generate_pages_recursive, source_to_destination


def main():
    source_to_destination("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
