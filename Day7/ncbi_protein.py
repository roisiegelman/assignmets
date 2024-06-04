import argparse
import csv
import os
from datetime import datetime
from Bio import Entrez
from Bio import SeqIO

def search_protein(email, term, max_items):
    Entrez.email = email  # Always tell NCBI who you are
    search_handle = Entrez.esearch(db="protein", term=term, retmax=max_items)
    search_results = Entrez.read(search_handle)
    search_handle.close()
    return search_results["IdList"], search_results["Count"]

def fetch_and_save_proteins(email, ids, out_dir):
    filenames = []
    for idx, protein_id in enumerate(ids):
        fetch_handle = Entrez.efetch(db="protein", id=protein_id, rettype="fasta", retmode="text")
        record = SeqIO.read(fetch_handle, "fasta")
        fetch_handle.close()
        
        filename = os.path.join(out_dir, f"{protein_id}.fasta")
        with open(filename, 'w') as file:
            SeqIO.write(record, file, "fasta")
        filenames.append(filename)
    return filenames

def log_search_details(term, max_items, total_found, filenames, log_file):
    fieldnames = ['Date', 'Search Term', 'Number Asked For', 'Total Items Found', 'Saved Files']
    file_exists = os.path.isfile(log_file)

    with open(log_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Search Term': term,
            'Number Asked For': max_items,
            'Total Items Found': total_found,
            'Saved Files': ", ".join(filenames)
        })

def print_csv_log(log_file):
    with open(log_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(', '.join(row))

def main():
    parser = argparse.ArgumentParser(description="Search for proteins in NCBI and download results.")
    parser.add_argument('--email', required=True, help='Email address (required by NCBI)')
    parser.add_argument('--term', required=True, help='Search term')
    parser.add_argument('--max_items', type=int, default=15, help='Maximum number of items to download')
    parser.add_argument('--out_dir', required=True, help='Output directory for saved files')
    parser.add_argument('--log_file', required=True, help='CSV file to log search details')

    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    ids, total_found = search_protein(args.email, args.term, args.max_items)
    filenames = fetch_and_save_proteins(args.email, ids, args.out_dir)
    log_search_details(args.term, args.max_items, total_found, filenames, args.log_file)

    for filename in filenames:
        print(filename)

    print("Search log:")
    print_csv_log(args.log_file)

if __name__ == "__main__":
    main()
