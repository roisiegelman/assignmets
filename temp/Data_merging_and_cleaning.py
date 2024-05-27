import pandas as pd

# Load the merged data
merged_data = pd.read_csv('merged_clinical_nsd1_data.csv')

# Print the column names before renaming
print("Columns before renaming:")
print(merged_data.columns.tolist())

# Rename the NSD1 column
merged_data.rename(columns={
    'NSD1: mRNA expression z-scores relative to all samples (log microarray)': 'NSD1'
}, inplace=True)

# Print the column names after renaming
print("Columns after renaming:")
print(merged_data.columns.tolist())

# Save the corrected merged data to a new CSV file
merged_data.to_csv('merged_clinical_nsd1_data_corrected.csv', index=False)

print("Corrected merged data saved to 'merged_clinical_nsd1_data_corrected.csv'")
