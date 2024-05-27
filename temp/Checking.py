import pandas as pd

# Load the cleaned data
data = pd.read_csv('cleaned_clinical_nsd1_data.csv')

# Print summary statistics of the relevant columns
print(data[['OS_MONTHS', 'OS_STATUS', 'NSD1']].describe())
print(data['OS_STATUS'].value_counts())

# Verify the split
high_expression = data[data['high_expression']]
low_expression = data[~data['high_expression']]

print("High expression group size:", high_expression.shape[0])
print("Low expression group size:", low_expression.shape[0])

print("High expression group survival times:")
print(high_expression['OS_MONTHS'].describe())

print("Low expression group survival times:")
print(low_expression['OS_MONTHS'].describe())