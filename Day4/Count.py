# Allows you to perform various file operations such as opening, reading, writing, and deleting files
import os

# Set directory
DEFAULT_DIRECTORY = "C:/Users/roisi/Course/assignmets/Day4"

def count_file_stats(filepath):
    try:
        with open(filepath, 'r') as file:
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
    filepath = os.path.join(DEFAULT_DIRECTORY, filename)
    count_file_stats(filepath)

if __name__ == "__main__":
    main()        