import requests
import pandas as pd
from lifelines import KaplanMeierFitter, statistics
import matplotlib.pyplot as plt
import numpy as np

# Function to fetch clinical data
def fetch_clinical_data(study_id):
    url = f'https://www.cbioportal.org/api/studies/{study_id}/clinical-data'
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())

# Function to fetch molecular profiles
def fetch_molecular_profiles(study_id):
    url = f'https://www.cbioportal.org/api/studies/{study_id}/molecular-profiles'
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())

# Function to fetch gene expression data
def fetch_gene_expression(study_id, gene, molecular_profile_id):
    url = f'https://www.cbioportal.org/api/molecular-profiles/{molecular_profile_id}/expression/fetch'
    headers = {'Content-Type': 'application/json'}
    params = {
        'geneList': [gene],
        'sampleListId': f'{study_id}_all'
    }
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data)

# Function to prepare data
def prepare_data(study_id, gene, subtype, molecular_profile_id):
    # Fetch clinical data
    clinical_data = fetch_clinical_data(study_id)
    
    # Fetch gene expression data
    expression_data = fetch_gene_expression(study_id, gene, molecular_profile_id)
    
    # Merge data
    merged_data = pd.merge(clinical_data, expression_data, left_on='PATIENT_ID', right_on='sampleId')
    
    # Filter by subtype
    if subtype:
        merged_data = merged_data[merged_data['CANCER_TYPE_DETAILED'] == subtype]
    
    # Clean and prepare data for survival analysis
    merged_data = merged_data[['PATIENT_ID', 'OS_MONTHS', 'OS_STATUS', gene]]
    merged_data = merged_data.dropna()
    
    return merged_data

# Function to plot Kaplan-Meier curves
def plot_kaplan_meier(data, gene):
    # Divide into high and low expression groups
    median_expression = data[gene].median()
    data['expression_group'] = np.where(data[gene] > median_expression, 'High', 'Low')
    
    # Fit Kaplan-Meier estimator
    kmf = KaplanMeierFitter()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for group in data['expression_group'].unique():
        group_data = data[data['expression_group'] == group]
        kmf.fit(group_data['OS_MONTHS'], event_observed=group_data['OS_STATUS'] == 'DECEASED', label=group)
        kmf.plot_survival_function(ax=ax)
    
    # Calculate p-value
    high_expression = data[data['expression_group'] == 'High']
    low_expression = data[data['expression_group'] == 'Low']
    results = statistics.logrank_test(high_expression['OS_MONTHS'], low_expression['OS_MONTHS'],
                                      event_observed_A=high_expression['OS_STATUS'] == 'DECEASED',
                                      event_observed_B=low_expression['OS_STATUS'] == 'DECEASED')
    
    p_value = results.p_value
    plt.title(f'Kaplan-Meier Curve for {gene} Expression\nP-value: {p_value:.4f}')
    plt.xlabel('Months')
    plt.ylabel('Survival Probability')
    plt.legend()
    plt.show()

# Main execution flow
if __name__ == '__main__':
    study_id = 'brca_metabric'
    gene = 'TP53'
    subtype = 'Lobular Carcinoma'
    
    # Fetch and print available molecular profiles
    molecular_profiles = fetch_molecular_profiles(study_id)
    print(molecular_profiles)
    
    # Assume the correct profile ID is 'brca_metabric_mrna'
    molecular_profile_id = 'brca_metabric_mrna'  # Adjust this based on the actual profile ID from the fetched profiles
    
    # Prepare data
    data = prepare_data(study_id, gene, subtype, molecular_profile_id)
    print(data.head())
    
    # Plot Kaplan-Meier curve
    plot_kaplan_meier(data, gene)
