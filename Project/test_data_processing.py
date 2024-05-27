import pytest
import pandas as pd
from io import StringIO
from data_processing import (
    load_and_rename_clinical_data,
    load_and_rename_nsd1_data,
    merge_data,
    save_data,
    clean_data
)

@pytest.fixture
def clinical_data_csv():
    return StringIO("""Study ID,Patient ID,Sample ID,Overall Survival (Months),Overall Survival Status,Pam50 + Claudin-low subtype
    brca_metabric,MB-0000,MB-0000,75.65,1:DECEASED,LumA
    brca_metabric,MB-0002,MB-0002,43.19,0:LIVING,LumB
    brca_metabric,MB-0005,MB-0005,48.87,1:DECEASED,Basal
    brca_metabric,MB-0006,MB-0006,47.68,0:LIVING,Her2
    brca_metabric,MB-0008,MB-0008,76.97,1:DECEASED,Normal
    """)

@pytest.fixture
def nsd1_data_csv():
    return StringIO("""Study ID,Patient ID,Sample ID,NSD1: mRNA expression z-scores relative to all samples (log microarray)
    brca_metabric,MB-0000,MB-0000,0.5
    brca_metabric,MB-0002,MB-0002,-0.3
    brca_metabric,MB-0005,MB-0005,1.2
    brca_metabric,MB-0006,MB-0006,0.8
    brca_metabric,MB-0008,MB-0008,-1.1
    """)

def test_load_and_rename_clinical_data(clinical_data_csv):
    renamed_clinical_data = load_and_rename_clinical_data(clinical_data_csv)
    assert 'OS_MONTHS' in renamed_clinical_data.columns
    assert 'OS_STATUS' in renamed_clinical_data.columns
    assert 'CLAUDIN_SUBTYPE' in renamed_clinical_data.columns

def test_load_and_rename_nsd1_data(nsd1_data_csv):
    renamed_nsd1_data = load_and_rename_nsd1_data(nsd1_data_csv)
    assert 'Sample_ID' in renamed_nsd1_data.columns
    assert 'NSD1' in renamed_nsd1_data.columns

def test_merge_data(clinical_data_csv, nsd1_data_csv):
    clinical_data = load_and_rename_clinical_data(clinical_data_csv)
    nsd1_data = load_and_rename_nsd1_data(nsd1_data_csv)
    merged_data = merge_data(clinical_data, nsd1_data)
    assert 'OS_MONTHS' in merged_data.columns
    assert 'NSD1' in merged_data.columns
    assert len(merged_data) == 5

def test_clean_data(clinical_data_csv, nsd1_data_csv):
    clinical_data = load_and_rename_clinical_data(clinical_data_csv)
    nsd1_data = load_and_rename_nsd1_data(nsd1_data_csv)
    merged_data = merge_data(clinical_data, nsd1_data)
    cleaned_data = clean_data(merged_data)
    assert not cleaned_data.isnull().values.any()

def test_save_data(tmp_path):
    test_data = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    save_path = tmp_path / "test_save_data.csv"
    save_data(test_data, save_path)
    loaded_data = pd.read_csv(save_path)
    pd.testing.assert_frame_equal(test_data, loaded_data)
