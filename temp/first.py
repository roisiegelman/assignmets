def fetch_clinical_attributes_list(study_id):
    url = f'https://www.cbioportal.org/api/studies/{study_id}/clinical-attributes'
    response = requests.get(url)
    response.raise_for_status()
    attributes = response.json()
    return pd.DataFrame(attributes)

# Fetch and print available clinical attributes
if __name__ == '__main__':
    study_id = 'brca_metabric'
    
    # Fetch available clinical attributes
    clinical_attributes = fetch_clinical_attributes_list(study_id)
    print("Available Clinical Attributes:")
    print(clinical_attributes)
