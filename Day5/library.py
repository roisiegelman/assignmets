# Allows you to perform various file operations such as opening, reading, writing, and deleting files
import os

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("File not found.")
        return None

def count_characters(text):
    return len(text)            

def count_lines(text):
    return text.count('\n') + 1  # Counting '\n' occurrences to get the number of lines
            
def count_words(text):
    return len(text.split()) #Splitting text by spaces to count words
           
def count_file_stats(filename):
    text = read_file(filename)
    if text:
        char_count = count_characters(text)
        line_count = count_lines(text)
        word_count = count_words(text)
        print(f"Character count: {char_count}")
        print(f"Line count: {line_count}")
        print(f"Word count: {word_count}")
