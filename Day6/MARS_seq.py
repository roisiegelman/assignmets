import pandas as pd
import gseapy as gp
from gseapy.plot import barplot
import matplotlib.pyplot as plt

# Path to the local Excel file and .gmt file
file_path = 'Roi_MARSseq.xlsx'
gmt_path = 'mh.all.v2023.2.Mm.symbols.gmt'  # Update with the actual path to the downloaded .gmt file

# Load the Excel file using openpyxl as the engine
print("Loading data...")
data = pd.read_excel(file_path, engine='openpyxl')
print("Data loaded successfully.")

# Display the first few rows of the dataframe to understand its structure
print("First few rows of the dataframe:")
print(data.head())

# Extract relevant columns
print("Extracting relevant columns...")
expression_data = data[['Unnamed: 0', 'No.I_1.rld', 'No.I_2.rld', 'No.I_3.rld', 'WT.sc_1.rld', 'WT.sc_2.rld', 'WT.sc_3.rld', 'KO.2_1.rld', 'KO.2_2.rld', 'KO.2_3.rld', 'KO.3_1.rld', 'KO.3_2.rld', 'KO.3_3.rld']]
differential_expression_data = data[['Unnamed: 0', 'WT_PyMT_NSD1_KO.log2FoldChange', 'WT_PyMT_NSD1_KO.pvalue', 'WT_PyMT_NSD1_KO.padj']]
print("Columns extracted.")

# Rename columns for easier access
expression_data.columns = ['Gene', 'No.I_1', 'No.I_2', 'No.I_3', 'WT.sc_1', 'WT.sc_2', 'WT.sc_3', 'KO.2_1', 'KO.2_2', 'KO.2_3', 'KO.3_1', 'KO.3_2', 'KO.3_3']
differential_expression_data.columns = ['Gene', 'log2FoldChange', 'pvalue', 'padj']
print("Columns renamed.")

# Rank genes based on log2 fold change
print("Ranking genes...")
ranked_genes = differential_expression_data.sort_values(by='log2FoldChange', ascending=False)

# Prepare the ranked list of genes and convert gene symbols to title case (first letter uppercase)
ranked_genes['Gene'] = ranked_genes['Gene'].astype(str).str.title()
ranked_gene_list = ranked_genes[['Gene', 'log2FoldChange']].set_index('Gene').squeeze()
print("Genes ranked.")

# Debugging: Print the first few genes to ensure they are title case
print("First few genes in ranked list:")
print(ranked_gene_list.head())

# Load the gene set file and print the first few entries to verify
print("Loading gene set file...")
with open(gmt_path, 'r') as file:
    first_line = file.readline()
    print("First entry in gene set file:")
    print(first_line)

# Run GSEA using the local .gmt file
print("Running GSEA...")
enr = gp.prerank(rnk=ranked_gene_list, gene_sets=gmt_path, min_size=1, max_size=5000, permutation_num=100, outdir=None, seed=6)
print("GSEA completed.")

# Inspect the results DataFrame
print("GSEA Results:")
print(enr.res2d.head())

# Check column names of the result DataFrame
print("Column names of GSEA results:")
print(enr.res2d.columns)

# Adjust column names based on actual names in the results
column_mapping = {'FDR q-val': 'Adjusted_P-value', 'NOM p-val': 'NOM_pval'}
enr.res2d.rename(columns=column_mapping, inplace=True)

# Verify renaming
print("Column names after renaming:")
print(enr.res2d.columns)

# Plot the distribution of nominal p-values if the column exists
if 'NOM_pval' in enr.res2d.columns:
    print("Plotting p-value distribution...")
    plt.hist(enr.res2d['NOM_pval'], bins=50, edgecolor='k', alpha=0.7)
    plt.xlabel('Nominal P-value')
    plt.ylabel('Frequency')
    plt.title('Distribution of Nominal P-values from GSEA')
    plt.show()
else:
    print("'NOM_pval' column not found in the GSEA results.")

# Lower the significance threshold to include more pathways in the plot
print("Filtering results with lower significance threshold...")
if 'Adjusted_P-value' in enr.res2d.columns:
    filtered_results = enr.res2d[enr.res2d['Adjusted_P-value'] < 0.25]  # Increase threshold to 0.25
    print("Filtered results:")
    print(filtered_results)
else:
    print("'Adjusted_P-value' column not found in the GSEA results.")
    print("Available columns: ", enr.res2d.columns)

# Check if there are any enriched terms
if filtered_results.empty:
    print("No enriched terms found even with a lower significance threshold.")
else:
    # Print the filtered results to verify before plotting
    print("Filtered results for plotting:")
    print(filtered_results.head())

    # Plot the top 20 enriched pathways
    print("Plotting results...")

    # Adjust the column name mapping for barplot
    filtered_results.columns = filtered_results.columns.str.replace('Adjusted_P-value', 'Adjusted P-value')

    # Create the barplot
    ax = barplot(filtered_results, title='Pathways Enriched in KO vs Control', top_term=20)
    plt.show()
    print("Plot displayed.")
