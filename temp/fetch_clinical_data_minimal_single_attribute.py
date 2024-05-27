import requests
import pandas as pd

def fetch_clinical_attributes(study_id, sample_list_id, attributes):
    url = f'https://www.cbioportal.org/api/clinical-data/fetch'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'studyId': study_id,
        'sampleListId': sample_list_id,
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

if __name__ == '__main__':
    study_id = 'brca_metabric'
    sample_list_id = 'brca_metabric_all'  # Use the verified sample list
    attributes = ['OS_MONTHS']  # Simplified to a single known attribute
    
    clinical_data = fetch_clinical_attributes(study_id, sample_list_id, attributes)
    print("Fetched Clinical Data:")
    print(clinical_data.head())
