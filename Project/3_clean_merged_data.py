import pandas as pd

# Load the corrected merged data
merged_data = pd.read_csv('merged_clinical_nsd1_data_corrected.csv')

# Drop rows with NaN values in the relevant columns
cleaned_data = merged_data.dropna(subset=['OS_MONTHS', 'OS_STATUS', 'CLAUDIN_SUBTYPE', 'NSD1'])

# Save the cleaned data to a new CSV file
cleaned_data.to_csv('cleaned_clinical_nsd1_data.csv', index=False)
print("Cleaned data saved to 'cleaned_clinical_nsd1_data.csv'")