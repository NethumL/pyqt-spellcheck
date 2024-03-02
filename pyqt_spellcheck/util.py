def find_word_bounds(text: str, cursor_pos: int) -> tuple[int, int]:
    """Find the start and end of the word under the cursor."""
    start = cursor_pos
    while start > 0 and text[start - 1].isalnum():
        start -= 1

    end = cursor_pos
    while end < len(text) and text[end].isalnum():
        end += 1

    return start, end
