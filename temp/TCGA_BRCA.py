import requests
import pandas as pd
import json
import os
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
import numpy as np

# Function to get TCGA clinical data
def get_tcga_clinical_data(project_id):
    url = 'https://api.gdc.cancer.gov/cases'
    filters = {
        "op": "and",
        "content": [
            {
                "op": "in",
                "content": {
                    "field": "cases.project.project_id",
                    "value": [project_id]
                }
            }
        ]
    }
    params = {
        'filters': json.dumps(filters),
        'fields': 'case_id,submitter_id,demographic,diagnoses.days_to_death,diagnoses.vital_status',
        'format': 'json',
        'size': '1000'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()['data']['hits']
    return pd.json_normalize(data)

# Function to search for TCGA gene expression files
def search_tcga_files(project_id, data_type="gene_expression_quantification"):
    url = 'https://api.gdc.cancer.gov/files'
    filters = {
        "op": "and",
        "content": [
            {
                "op": "in",
                "content": {
                    "field": "cases.project.project_id",
                    "value": [project_id]
                }
            },
            {
                "op": "in",
                "content": {
                    "field": "files.data_type",
                    "value": [data_type]
                }
            },
            {
                "op": "in",
                "content": {
                    "field": "files.experimental_strategy",
                    "value": ["RNA-Seq"]
                }
            }
        ]
    }
    params = {
        'filters': json.dumps(filters),
        'fields': 'file_id,file_name,cases.case_id,cases.samples.sample_type',
        'format': 'json',
        'size': '100'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()['data']['hits']
    return pd.json_normalize(data)

# Function to download TCGA files
def download_file(file_id, file_name):
    url = f'https://api.gdc.cancer.gov/data/{file_id}'
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(file_name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

# Placeholder for processing RNA-Seq data files
def process_expression_data(file_names):
    # This function should be replaced with actual logic to process the downloaded RNA-Seq files
    # Here we return a sample dataframe for demonstration
    expression_data = {
        'case_id': ['case1', 'case2', 'case3', 'case4', 'case5'],
        'NSD1': [2.5, 3.0, 2.8, 2.2, 3.5]
    }
    return pd.DataFrame(expression_data)

# Function to plot Kaplan-Meier curves
def plot_kaplan_meier(data, gene, subtype=None):
    kmf = KaplanMeierFitter()
    
    if subtype:
        data = data[data['diagnoses.primary_diagnosis'].str.contains(subtype, case=False, na=False)]
    
    median_expression = data[gene].median()
    data['expression_group'] = np.where(data[gene] > median_expression, 'High', 'Low')
    
    for group in data['expression_group'].unique():
        group_data = data[data['expression_group'] == group]
        kmf.fit(group_data['diagnoses.days_to_death'], event_observed=group_data['diagnoses.vital_status'] == 'Dead', label=group)
        kmf.plot_survival_function()
    
    plt.title(f'Kaplan-Meier Curve for {gene}{" in " + subtype if subtype else ""}')
    plt.xlabel('Days')
    plt.ylabel('Survival Probability')
    plt.show()

# Main execution flow
if __name__ == '__main__':
    project_id = 'TCGA-BRCA'
    gene_of_interest = 'NSD1'
    
    # Step 1: Fetch clinical data
    tcga_clinical_data = get_tcga_clinical_data(project_id)
    print(tcga_clinical_data.head())

    # Step 2: Search for gene expression files
    tcga_files = search_tcga_files(project_id)
    print(tcga_files.head())
    print(tcga_files.columns)  # Print columns to debug missing 'file_name' issue

    # Step 3: Download and process gene expression files
    # Here we assume downloading and processing only one file for demonstration
    # In practice, download all relevant files and process them
    for index, row in tcga_files.iterrows():
        file_id = row['file_id']
        if 'file_name' in row:
            file_name = row['file_name']
        else:
            file_name = file_id  # Use file_id if file_name is not available
        download_file(file_id, file_name)
        # Note: Add your actual processing logic here to handle the downloaded file
    
    # Placeholder for actual processing function
    tcga_expression_data = process_expression_data(tcga_files['file_id'])  # Adjust this line based on available data
    print(tcga_expression_data.head())

    # Step 4: Merge clinical and expression data
    tcga_merged_data = pd.merge(tcga_expression_data, tcga_clinical_data, on='case_id')
    print(tcga_merged_data.head())

    # Step 5: Plot Kaplan-Meier curve
    plot_kaplan_meier(tcga_merged_data, gene_of_interest)

    # Optional: Plot Kaplan-Meier curve for specific subtypes
    plot_kaplan_meier(tcga_merged_data, gene_of_interest, subtype='Lobular carcinoma')
