# DNA sequence analysis detailed explanation

###  Overview
This program analyzes a DNA sequence from a file in FASTA format. It provides two types of analyses:

**1.  Longest Repeated Sub-sequence:** Finds the longest sub-sequence that appears more than once in the DNA sequence.
  
**2.Longest Palindromic Sub-sequence:** Finds the longest sub-sequence that reads the same forwards and backwards.


###  Requirmnets:
**1. Python 3.x**

**2. Biopython library:** This is used for reading and parsing the FASTA file.
   * Execute the script `data_processing.py`
  ```python
 data_processing.py
```
### Installation
Before running the script, ensure you have Python 3 and Biopython installed. You can install Biopython using pip:
   ``` python
pip install biopython
```
**3. analyse the data**
 * Execute the script `data_analysis.py`
  ```python
 data_analysis.py
```
   * The script will yield a figure with 2 panels: Kaplan-Meier plot and barplot of the enriched pathwats
   * Detailed explanations and requirements can be found in [`data_analysis_explained.md`](https://github.com/roisiegelman/Project/blob/main/data_analysis_explained.md)
   * Testing the script:
   ```python
pytest test_data_analysis.py
```



This project was originally implemented as part of the [Python programming course](https://github.com/szabgab/wis-python-course-2024-04) at the [Weizmann Institute of Science](https://www.weizmann.ac.il/) taught by [Gabor Szabo](https://szabgab.com/).
