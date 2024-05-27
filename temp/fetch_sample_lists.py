import requests

def fetch_sample_lists(study_id):
    url = f'https://www.cbioportal.org/api/studies/{study_id}/sample-lists'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    study_id = 'brca_metabric'
    sample_lists = fetch_sample_lists(study_id)
    print("Available Sample Lists:")
    for sample_list in sample_lists:
        print(sample_list)
