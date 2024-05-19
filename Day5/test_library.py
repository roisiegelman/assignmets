from library import read_file, count_characters, count_lines, count_words

def test_read_file():
    content = read_file("example_file.txt")
    assert content is not None
    assert isinstance(content, str)

def test_count_characters():
    text = "Hello, world!"
    assert count_characters(text) == 13

def test_count_lines():
    text = "Line 1\nLine 2\nLine 3"
    assert count_lines(text) == 4

def test_count_words():
    text = "This is a test sentence."
    assert count_words(text) == 5
