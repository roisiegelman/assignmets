# DNA sequence analysis detailed explanation

###  Overview
This program analyzes a DNA sequence from a file in FASTA format. It provides two types of analyses:

**1.  Longest Repeated Sub-sequence:** Finds the longest sub-sequence that appears more than once in the DNA sequence.
  
**2.Longest Palindromic Sub-sequence:** Finds the longest sub-sequence that reads the same forwards and backwards.


###  Technical steps:
**1. Export data from [cBioPrtal](https://www.cbioportal.org/)**
    * Choose a database according to the cancer type. In this project, I investigated the data from [METABRIC](https://www.cbioportal.org/study/summary?id=brca_metabric)
    * Download clinical data and expression levels of the gene of choice. I chose *NSD1*
    * Download survival and mRNA expression data for groups with different expression levels of the gene of interest for each subtype separately. One might opt to compare data using either the median or quartiles. 
      I chose to compare the *bottom and the top quartiles of the expression of NSD1 and compare Luminal A (LumA), Luminal B(LumB) and Basal-like (Basal)*

**2. Coordinate the loading, merging, cleaning, and saving of the data by** 
   * Execute the script `data_processing.py`
  ```python
 data_processing.py
```
   * The script will yield `cleaned_clinical_nsd1_data.csv` that will be used in the next part
   * Detailed explanations and requirements can be found in [`data_processing_explained.md`](https://github.com/roisiegelman/Project/blob/main/data_processing_explained.md)
   * Testing the script:
   ``` python
pytest test_data_processing.py
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
