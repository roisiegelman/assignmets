import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook

def generate_barplot(file_path="Roi_MARSseq.xlsx"):
    # Load the data from the Excel file
    data = pd.read_excel(file_path, sheet_name=0)

    # Extract relevant columns
    data = data[['Unnamed: 0', 'WT_PyMT_NSD1_KO.log2FoldChange', 'WT_PyMT_NSD1_KO.pvalue']]
    data.columns = ['Gene', 'log2FoldChange', 'pvalue']

    # Filter for significant results (Pvalue <= 0.05)
    significant_data = data[data['pvalue'] <= 0.05]

    # Separate the data into control group (WT_PyMT) and KO group (NSD1_KO)
    control_group = significant_data[significant_data['log2FoldChange'] > 0].nlargest(10, 'log2FoldChange')
    ko_group = significant_data[significant_data['log2FoldChange'] < 0].nsmallest(10, 'log2FoldChange')

    # Create the bar plot
    plt.figure(figsize=(10, 8))

    # Horizontal bar plot
    plt.barh(control_group['Gene'], control_group['log2FoldChange'], color='blue', label='WT_PyMT')
    plt.barh(ko_group['Gene'], ko_group['log2FoldChange'], color='red', label='NSD1_KO')

    plt.xlabel('log2 Fold Change')
    plt.ylabel('Gene')
    plt.title('Top 10 Differentially Expressed Genes in WT_PyMT and NSD1_KO')
    plt.legend()

    # Save the plot
    plt.savefig('top_genes_barplot.png')
    plt.close()

if __name__ == "__main__":
    generate_barplot()
    # Display the plot
    img = plt.imread('top_genes_barplot.png')
    plt.imshow(img)
    plt.axis('off')
    plt.show()
