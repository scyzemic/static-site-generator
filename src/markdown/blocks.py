import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if not isinstance(block, str):
        raise TypeError("Expected block to be a string")

    match block:
        case block if re.match(r"^#{1,6}\s", block):
            return BlockType.HEADING
        case block if block.startswith("```") and block.endswith("```"):
            return BlockType.CODE
        case block if block.startswith("> "):
            return BlockType.QUOTE
        case block if block.startswith("- "):
            return BlockType.UNORDERED_LIST
        case block if block.startswith("1. "):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise TypeError("Expected markdown to be a string")

    blocks = markdown.split("\n\n")
    stripped_blocks = list(map(str.strip, blocks))
    non_empty_blocks = list(filter(lambda x: len(x) > 0, stripped_blocks))

    return non_empty_blocks
