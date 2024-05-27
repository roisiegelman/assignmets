import pandas as pd

# Load the clinical data
clinical_data = pd.read_csv('brca_metabric_clinical_data.csv')

# Ensure the clinical data has the correct column names
clinical_data.rename(columns={
    'Overall Survival (Months)': 'OS_MONTHS',
    'Overall Survival Status': 'OS_STATUS',
    'Pam50 + Claudin-low subtype': 'CLAUDIN_SUBTYPE'
}, inplace=True)

# Load the NSD1 expression data
nsd1_data = pd.read_csv('NSD1_mRNA_expression.csv')

# Ensure the NSD1 expression data has the correct column names
nsd1_data.rename(columns={
    'Sample ID': 'Sample_ID',
    'NSD1': 'NSD1'
}, inplace=True)

# Merge the clinical data with the NSD1 expression data on 'Sample_ID'
merged_data = pd.merge(clinical_data, nsd1_data, left_on='Sample ID', right_on='Sample_ID')

# Save the merged data to a new CSV file
merged_data.to_csv('merged_clinical_nsd1_data.csv', index=False)

print("Merged data saved to 'merged_clinical_nsd1_data.csv'")
