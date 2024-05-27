from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
import numpy as np

# Merge TCGA clinical and expression data
tcga_merged_data = pd.merge(tcga_expression_data, tcga_clinical_data, left_on='case_id', right_on='case_id')

# Define a function to plot Kaplan-Meier curves
def plot_kaplan_meier(data, gene, subtype=None):
    kmf = KaplanMeierFitter()
    
    if subtype:
        data = data[data['primary_diagnosis'].str.contains(subtype, case=False, na=False)]
    
    median_expression = data[gene].median()
    data['expression_group'] = np.where(data[gene] > median_expression, 'High', 'Low')
    
    for group in data['expression_group'].unique():
        group_data = data[data['expression_group'] == group]
        kmf.fit(group_data['days_to_death'], event_observed=group_data['vital_status'] == 'Dead', label=group)
        kmf.plot_survival_function()
    
    plt.title(f'Kaplan-Meier Curve for {gene}{" in " + subtype if subtype else ""}')
    plt.xlabel('Days')
    plt.ylabel('Survival Probability')
    plt.show()

# Plot Kaplan-Meier curve for TCGA data
plot_kaplan_meier(tcga_merged_data, 'normalized_count')

# Plot Kaplan-Meier curve for a specific subtype in TCGA data
plot_kaplan_meier(tcga_merged_data, 'normalized_count', subtype='Lobular carcinoma')

# Similarly, you can process and plot METABRIC data
metabric_merged_data = pd.merge(metabric_expression_data, metabric_clinical_data, left_on='sampleId', right_on='PATIENT_ID')
plot_kaplan_meier(metabric_merged_data, 'value')
