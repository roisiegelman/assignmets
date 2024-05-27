import pandas as pd

# Load the clinical data
clinical_data = pd.read_csv('brca_metabric_clinical_data.csv')

# Load the NSD1 expression data
nsd1_data = pd.read_csv('NSD1_mRNA_expression.csv')

# Merge the clinical data with the NSD1 expression data on 'Sample ID'
merged_data = pd.merge(clinical_data, nsd1_data, on='Sample ID')

# Save the merged data to a new CSV file
merged_data.to_csv('merged_clinical_nsd1_data.csv', index=False)

print("Merged data saved to 'merged_clinical_nsd1_data.csv'")
