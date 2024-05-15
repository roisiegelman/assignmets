# Allows you to perform various file operations such as opening, reading, writing, and deleting files
import os

def count_file_stats(filename):
    try:
        with open(filename, 'r') as file:
            text = file.read()
            char_count = len(text)
            line_count = text.count('\n') + 1  # Counting '\n' occurrences to get the number of lines
            word_count = len(text.split())  # Splitting text by spaces to count words
            print(f"Character count: {char_count}")
            print(f"Line count: {line_count}")
            print(f"Word count: {word_count}")
    except FileNotFoundError:
        print("File not found.")

def main():
    filename = input("Enter the filename: ")
    count_file_stats(filename)

if __name__ == "__main__":
    main()
