import pandas as pd
import matplotlib.pyplot as plt
import sys

def generate_barplot_from_excel(excel_file):
    data = pd.read_excel(excel_file)

    # Extracting relevant columns
    data = data[['Unnamed: 0', 'WT_PyMT_NSD1_KO.log2FoldChange', 'WT_PyMT_NSD1_KO.pvalue']]
    data.columns = ['Gene', 'log2FoldChange', 'Pvalue']

    # Filtering significant results
    significant_data = data[data['Pvalue'] <= 0.05]

    # Splitting data into two groups
    control_group = significant_data[significant_data['log2FoldChange'] > 0].nlargest(10, 'log2FoldChange')
    ko_group = significant_data[significant_data['log2FoldChange'] < 0].nsmallest(10, 'log2FoldChange')

    # Plotting the results
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(control_group['Gene'], control_group['log2FoldChange'], color='blue', label='WT_PyMT')
    ax.barh(ko_group['Gene'], ko_group['log2FoldChange'], color='red', label='NSD1_KO')
    ax.set_xlabel('log2FoldChange')
    ax.set_title('Top 10 Differentially Expressed Genes')
    ax.legend()
    plt.tight_layout()
    plt.savefig('differentially_expressed_genes.png')
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_barplot.py <excel_file>")
    else:
        excel_file = sys.argv[1]
        generate_barplot_from_excel(excel_file)
