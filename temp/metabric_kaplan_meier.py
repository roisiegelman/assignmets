import requests
import pandas as pd
from lifelines import KaplanMeierFitter, statistics
import matplotlib.pyplot as plt
import numpy as np

# Function to fetch clinical data with specific attributes
def fetch_clinical_attributes(study_id, attributes):
    url = f'https://www.cbioportal.org/api/clinical-data/fetch'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'studyId': study_id,
        'sampleListId': f'{study_id}_all',
        'attributes': attributes
    }
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"Request URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Request Payload: {payload}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Content-Length: {response.headers.get('Content-Length')}")
    print(f"Response Content-Type: {response.headers.get('Content-Type')}")
    print(f"Response Encoding: {response.encoding}")
    print(f"Response Text: {response.text[:1000]}")  # Print first 1000 characters of the response text

    if response.status_code != 200:
        print(f"Response Text: {response.text}")
        response.raise_for_status()

    if response.headers.get('Content-Length') == '0':
        print("Error: No content returned in response.")
        return pd.DataFrame()  # Return empty DataFrame if no data is returned

    try:
        data = response.json()
    except ValueError:
        print("Error: Response content is not valid JSON.")
        print(f"Response Text: {response.text}")
        return pd.DataFrame()  # Return empty DataFrame if no data is returned

    if not data:
        print("Error: No clinical data returned.")
        return pd.DataFrame()  # Return empty DataFrame if no data is returned

    df = pd.DataFrame(data)
    print("Clinical data columns:", df.columns)
    return df

# Function to fetch molecular profiles
def fetch_molecular_profiles(study_id):
    url = f'https://www.cbioportal.org/api/studies/{study_id}/molecular-profiles'
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())

# Function to fetch gene expression data
def fetch_gene_expression(molecular_profile_id, gene):
    # Fetch Entrez gene ID for the gene symbol
    gene_info_url = f'https://www.cbioportal.org/api/genes/{gene}'
    gene_info_response = requests.get(gene_info_url)
    gene_info_response.raise_for_status()
    gene_info = gene_info_response.json()
    entrez_gene_id = gene_info['entrezGeneId']
    
    url = f'https://www.cbioportal.org/api/molecular-profiles/{molecular_profile_id}/molecular-data/fetch'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'entrezGeneIds': [entrez_gene_id],
        'sampleListId': 'brca_metabric_all'
    }
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"Request URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Request Payload: {payload}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text[:1000]}")  # Print first 1000 characters of the response text
    if response.status_code != 200:
        print(f"Response Text: {response.text}")
        response.raise_for_status()
    
    data = response.json()
    df = pd.DataFrame(data)
    print("Expression data columns:", df.columns)
    return df

# Function to prepare data
def prepare_data(study_id, gene, subtype, molecular_profile_id):
    # Attributes to fetch from clinical data
    attributes = ['OS_MONTHS', 'OS_STATUS', 'CLAUDIN_SUBTYPE']
    
    # Fetch clinical data
    clinical_data = fetch_clinical_attributes(study_id, attributes)
    if clinical_data.empty:
        raise ValueError("Clinical data is empty. Please check the data fetching process.")
    
    print("Fetched Clinical Data:")
    print(clinical_data.head())
    
    # Fetch gene expression data
    expression_data = fetch_gene_expression(molecular_profile_id, gene)
    print("Fetched Gene Expression Data:")
    print(expression_data.head())
    
    # Check if necessary columns are present
    if 'patientId' not in clinical_data.columns:
        raise KeyError("Error: 'patientId' column not found in clinical data.")
    if 'sampleId' not in expression_data.columns:
        raise KeyError("Error: 'sampleId' column not found in expression data.")
    
    # Merge data
    merged_data = pd.merge(clinical_data, expression_data, left_on='patientId', right_on='sampleId')
    print("Merged Data Columns:", merged_data.columns)
    print("Merged Data Sample:")
    print(merged_data.head())
    
    # Filter by subtype
    subtype_column = 'CLAUDIN_SUBTYPE'
    if subtype:
        if subtype_column not in merged_data.columns:
            raise KeyError(f"Error: '{subtype_column}' column not found in merged data.")
        else:
            merged_data = merged_data[merged_data[subtype_column] == subtype]
    
    # Inspect merged data columns
    print("Merged data columns after filtering:", merged_data.columns)
    
    # Clean and prepare data for survival analysis
    if all(col in merged_data.columns for col in ['patientId', 'OS_MONTHS', 'OS_STATUS', 'value']):
        merged_data = merged_data[['patientId', 'OS_MONTHS', 'OS_STATUS', 'value']]
        merged_data.rename(columns={'value': gene}, inplace=True)
        merged_data = merged_data.dropna()
    else:
        raise KeyError("Required columns missing for survival analysis.")
    
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
    subtype = 'LumA'  # Change this to the desired subtype
    
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
