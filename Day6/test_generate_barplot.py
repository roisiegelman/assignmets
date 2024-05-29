import pytest
import os
from generate_barplot import generate_barplot
import matplotlib

def test_generate_barplot():
    # Use the 'Agg' backend to prevent plot display during tests
    matplotlib.use('Agg')

    # Ensure the plot is generated without user interaction
    generate_barplot()
    assert os.path.exists("top_genes_barplot.png")
