from utils.helpers import source_to_destination, generate_page


def main():
    source_to_destination("static", "public")
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html",
    )


if __name__ == "__main__":
    main()
