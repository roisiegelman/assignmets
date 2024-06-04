ncbi_protein.py: Search for "nsd1" in the NCBI protein database with this script. It will download up to the number of protein sequences specified, save each sequence in its own file, and keepa log of the search information in a CSV file.

the script contains the following functions


**search_protein:** Searches the NCBI protein database for the given term and returns up to max_items IDs and the total number of items found.
Fetch and save proteins:

**fetch_and_save_proteins:** Fetches each protein by ID and saves it in the specified output directory. Returns a list of filenames.
Log search details:

**log_search_details:** Logs the search term, number of items requested, total items found, and the names of saved files in a CSV file. If the log file doesn't exist, it creates one and writes the header.
Print CSV log:

**print_csv_log:** Reads the CSV log file and prints its content.

You can run the script with any number of items and show the search log by using the command line and giving it suitable arguments. As an example:
  _python ncbi_protein.py --email roi.siegelman@weizmann.ac.il --term nsd1 --max_items 7 --out_dir proteins --log_file search_log.csv_
