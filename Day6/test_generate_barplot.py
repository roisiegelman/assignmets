import pytest
import os
import warnings
from generate_barplot import generate_barplot_from_excel

@pytest.fixture
def setup_excel_file():
    excel_file = 'Roi_MARSseq.xlsx'
    yield excel_file
    # Cleanup if necessary
    if os.path.exists('differentially_expressed_genes.png'):
        os.remove('differentially_expressed_genes.png')

@pytest.mark.filterwarnings("ignore:.*datetime.datetime.utcnow.*:DeprecationWarning")
def test_generate_barplot(setup_excel_file):
    excel_file = setup_excel_file
    generate_barplot_from_excel(excel_file)
    assert os.path.exists('differentially_expressed_genes.png')
