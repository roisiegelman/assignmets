from Bio import SeqIO
import argparse

def find_longest_repeated_subsequence(sequence):
    n = len(sequence)
    longest_subseq = ""
    
    # Use a suffix array approach for efficiency
    suffixes = sorted([sequence[i:] for i in range(n)])
    
    for i in range(n - 1):
        # Find the longest common prefix of suffixes[i] and suffixes[i+1]
        lcp = ""
        for x, y in zip(suffixes[i], suffixes[i + 1]):
            if x == y:
                lcp += x
            else:
                break
        if len(lcp) > len(longest_subseq):
            longest_subseq = lcp
            
    return longest_subseq

def find_longest_palindromic_subsequence(sequence):
    def expand_around_center(s, left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    longest_palindrome = ""
    for i in range(len(sequence)):
        # Odd length palindromes
        palindrome1 = expand_around_center(sequence, i, i)
        # Even length palindromes
        palindrome2 = expand_around_center(sequence, i, i + 1)

        # Update the longest palindrome found
        if len(palindrome1) > len(longest_palindrome):
            longest_palindrome = palindrome1
        if len(palindrome2) > len(longest_palindrome):
            longest_palindrome = palindrome2

    return longest_palindrome

def parse_sequence(file_path):
    record = SeqIO.read(file_path, "fasta")
    return str(record.seq)

def main():
    parser = argparse.ArgumentParser(description="Sequence analysis tool")
    parser.add_argument("fasta_file", help="Path to the input file in FASTA format")
    parser.add_argument("--longest", action="store_true", help="Find the longest repeated sub-sequence")
    parser.add_argument("--palindrome", action="store_true", help="Find the longest palindromic sub-sequence")
    
    args = parser.parse_args()
    
    try:
        sequence = parse_sequence(args.fasta_file)
        print("Sequence loaded successfully.")
    except Exception as e:
        print(f"Error reading sequence: {e}")
        return
    
    if args.longest:
        longest_repeat = find_longest_repeated_subsequence(sequence)
        print("Longest repeated sub-sequence:", longest_repeat)
    
    if args.palindrome:
        longest_palindrome = find_longest_palindromic_subsequence(sequence)
        print("Longest palindromic sub-sequence:", longest_palindrome)

if __name__ == "__main__":
    main()
