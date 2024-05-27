import pandas as pd

def load_and_rename_clinical_data(clinical_data_path):
    """Load and rename columns in the clinical data."""
    clinical_data = pd.read_csv(clinical_data_path)
    clinical_data.rename(columns={
        'Overall Survival (Months)': 'OS_MONTHS',
        'Overall Survival Status': 'OS_STATUS',
        'Pam50 + Claudin-low subtype': 'CLAUDIN_SUBTYPE'
    }, inplace=True)
    return clinical_data

def load_and_rename_nsd1_data(nsd1_data_path):
    """Load and rename columns in the NSD1 expression data."""
    nsd1_data = pd.read_csv(nsd1_data_path)
    nsd1_data.rename(columns={
        'Sample ID': 'Sample_ID',
        'NSD1: mRNA expression z-scores relative to all samples (log microarray)': 'NSD1'
    }, inplace=True)
    return nsd1_data

def merge_data(clinical_data, nsd1_data):
    """Merge clinical data with NSD1 expression data."""
    merged_data = pd.merge(clinical_data, nsd1_data, left_on='Sample ID', right_on='Sample_ID')
    return merged_data

def save_data(data, path):
    """Save data to a CSV file."""
    data.to_csv(path, index=False)
    print(f"Data saved to '{path}'")

def clean_data(merged_data):
    """Drop rows with NaN values in the relevant columns."""
    cleaned_data = merged_data.dropna(subset=['OS_MONTHS', 'OS_STATUS', 'CLAUDIN_SUBTYPE', 'NSD1'])
    return cleaned_data

def main():
    clinical_data_path = 'brca_metabric_clinical_data.csv'
    nsd1_data_path = 'NSD1_mRNA_expression.csv'
    merged_data_path = 'merged_clinical_nsd1_data.csv'
    corrected_data_path = 'merged_clinical_nsd1_data_corrected.csv'
    cleaned_data_path = 'cleaned_clinical_nsd1_data.csv'

    # Load and rename data
    clinical_data = load_and_rename_clinical_data(clinical_data_path)
    nsd1_data = load_and_rename_nsd1_data(nsd1_data_path)

    # Merge data
    merged_data = merge_data(clinical_data, nsd1_data)

    # Save merged data
    save_data(merged_data, merged_data_path)

    # Rename NSD1 column if necessary (redundant step here as it's already renamed)
    merged_data.rename(columns={
        'NSD1': 'NSD1'
    }, inplace=True)

    # Save corrected merged data
    save_data(merged_data, corrected_data_path)

    # Clean data
    cleaned_data = clean_data(merged_data)

    # Save cleaned data
    save_data(cleaned_data, cleaned_data_path)

if __name__ == "__main__":
    main()
