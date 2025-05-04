from textnode import TextNode, TextType


def main():
    print(TextNode("This is some text", TextType.BOLD, "https://example.com"))


if __name__ == "__main__":
    main()
