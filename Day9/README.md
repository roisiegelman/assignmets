# DNA sequence analysis detailed explanation

###  Overview
This program analyzes a DNA sequence from a file in FASTA format. It provides two types of analyses:

**1.  Longest Repeated Sub-sequence:** Finds the longest sub-sequence that appears more than once in the DNA sequence.
  
**2.Longest Palindromic Sub-sequence:** Finds the longest sub-sequence that reads the same forwards and backwards.


###  Requirmnets:
**1. Python 3.x**

**2. Biopython library:** This is used for reading and parsing the FASTA file.

### Installation
Before running the script, ensure you have Python 3 and Biopython installed. You can install Biopython using pip:
   ``` python
pip install biopython
```
### Functionality
1.  **find_longest_repeated_subsequence(sequence):**
This function identifies the longest sub-sequence that repeats itself within the DNA sequence.
It creates suffixes of the sequence, sorts them, and then finds the longest common prefix between consecutive suffixes.

2.  **find_longest_palindromic_subsequence(sequence):**
This function finds the longest palindromic sub-sequence.
It uses an "expand around center" technique to identify palindromes efficiently.

3.  **parse_sequence(file_path):**
This function reads and parses the DNA sequence from a FASTA file using Biopython's SeqIO module.

4.  **main():**
This is the entry point of the script. It handles command-line arguments, reads the sequence from the input file, and performs the specified analyses.

## Usage
Run the script from the command line, specifying the path to your FASTA file and the desired analyses.

 ### Example Command:
  ```python
 python analyze.py sequence.fasta --longest --palindrome
```
### Arguments:
* `fasta_file`: The path to the input file in FASTA format.
* `--longest`: (Optional) Perform analysis to find the longest repeated sub-sequence.
* `--palindrome`: (Optional) Perform analysis to find the longest palindromic sub-sequence.

### Example Output:
   ```python
Sequence loaded successfully.
Longest repeated sub-sequence: ACACCACAGGCTGA
Longest palindromic sub-sequence: GTCAATG
```
### Summary
This script provides a flexible and efficient way to analyze DNA sequences for specific features. Users can choose to analyze for the longest repeated sub-sequence, the longest palindromic sub-sequence, or both, by using the appropriate command-line arguments. The script ensures robust handling of input files and sequences through Biopython, making it suitable for various DNA sequence analysis tasks.
