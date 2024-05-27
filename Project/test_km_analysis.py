import pytest
import pandas as pd
from km_analysis import load_data, ensure_columns_present, convert_os_status, limit_months, create_expression_groups

def test_load_data():
    data = load_data('cleaned_clinical_nsd1_data.csv')
    assert not data.empty
    assert isinstance(data, pd.DataFrame)

def test_ensure_columns_present():
    data = pd.DataFrame({
        'OS_MONTHS': [1, 2, 3],
        'OS_STATUS': ['1:DECEASED', '0:LIVING', '1:DECEASED'],
        'CLAUDIN_SUBTYPE': ['subtype1', 'subtype2', 'subtype3'],
        'NSD1': [0.1, 0.2, 0.3]
    })
    ensure_columns_present(data, ['OS_MONTHS', 'OS_STATUS', 'CLAUDIN_SUBTYPE', 'NSD1'])

def test_convert_os_status():
    data = pd.DataFrame({
        'OS_STATUS': ['1:DECEASED', '0:LIVING', '1:DECEASED']
    })
    result = convert_os_status(data)
    assert 'event' in result.columns
    assert result['event'].tolist() == [1, 0, 1]

def test_limit_months():
    data = pd.DataFrame({
        'OS_MONTHS': [10, 20, 30, 40],
        'OS_STATUS': ['1:DECEASED', '0:LIVING', '1:DECEASED', '0:LIVING'],
        'CLAUDIN_SUBTYPE': ['Subtype1', 'Subtype2', 'Subtype1', 'Subtype2'],
        'NSD1': [2.5, 3.0, 1.0, 4.5]
    })
    
    # Limit to 30 months
    result = limit_months(data, 30)
    
    expected_result = pd.DataFrame({
        'OS_MONTHS': [10, 20, 30],
        'OS_STATUS': ['1:DECEASED', '0:LIVING', '1:DECEASED'],
        'CLAUDIN_SUBTYPE': ['Subtype1', 'Subtype2', 'Subtype1'],
        'NSD1': [2.5, 3.0, 1.0]
    })
    
    assert result.equals(expected_result), f"Expected {expected_result} but got {result}"

def test_create_expression_groups_median():
    data = pd.DataFrame({
        'NSD1': [0.1, 0.2, 0.3, 0.4]
    })
    result = create_expression_groups(data, 'NSD1', 1)
    assert 'high_expression' in result.columns
    assert result['high_expression'].tolist() == [False, False, True, True]

def test_create_expression_groups_quartiles():
    data = pd.DataFrame({
        'NSD1': [0.1, 0.2, 0.3, 0.4]
    })
    result = create_expression_groups(data, 'NSD1', 2)
    assert 'high_expression' in result.columns
    assert 'low_expression' in result.columns
    
    # Determine the quartile threshold values for the test data
    top_quartile_threshold = data['NSD1'].quantile(0.75)
    bottom_quartile_threshold = data['NSD1'].quantile(0.25)
    
    # Expected results based on the quantile thresholds
    expected_high_expression = data['NSD1'] >= top_quartile_threshold
    expected_low_expression = data['NSD1'] <= bottom_quartile_threshold
    
    assert result['high_expression'].tolist() == expected_high_expression.tolist()
    assert result['low_expression'].tolist() == expected_low_expression.tolist()
