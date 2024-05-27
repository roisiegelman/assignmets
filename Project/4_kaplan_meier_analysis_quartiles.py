import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

# Load the cleaned merged data
data = pd.read_csv('cleaned_clinical_nsd1_data.csv')

# Ensure the necessary columns are present
required_columns = ['OS_MONTHS', 'OS_STATUS', 'CLAUDIN_SUBTYPE', 'NSD1']
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"Missing one or more required columns: {required_columns}")

# Convert 'OS_STATUS' to a binary event: 1 if 'DECEASED', 0 otherwise
data['event'] = data['OS_STATUS'].apply(lambda x: 1 if x == '1:DECEASED' else 0)

# Limit the months to 200
data = data[data['OS_MONTHS'] <= 200]

# Set thresholds for top and bottom quartiles of NSD1 expression
gene_expression = 'NSD1'
top_quartile_threshold = data[gene_expression].quantile(0.75)
bottom_quartile_threshold = data[gene_expression].quantile(0.25)

# Create groups based on top and bottom quartiles
data['top_quartile'] = data[gene_expression] >= top_quartile_threshold
data['bottom_quartile'] = data[gene_expression] <= bottom_quartile_threshold

# Perform Kaplan-Meier analysis for the entire cohort
kmf = KaplanMeierFitter()

fig, ax = plt.subplots()

# Fit the Kaplan-Meier estimator for the high expression group
kmf.fit(durations=data[data['top_quartile']]['OS_MONTHS'], 
        event_observed=data[data['top_quartile']]['event'], 
        label='Top Quartile Expression')
kmf.plot_survival_function(ax=ax)

# Fit the Kaplan-Meier estimator for the low expression group
kmf.fit(durations=data[data['bottom_quartile']]['OS_MONTHS'], 
        event_observed=data[data['bottom_quartile']]['event'], 
        label='Bottom Quartile Expression')
kmf.plot_survival_function(ax=ax)

plt.title(f'Kaplan-Meier Survival Curve for {gene_expression} Expression (Entire Cohort)')
plt.xlabel('Months')
plt.ylabel('Survival Probability')

# Log-rank test to compare the survival distributions
results = logrank_test(
    data[data['top_quartile']]['OS_MONTHS'], 
    data[data['bottom_quartile']]['OS_MONTHS'], 
    event_observed_A=data[data['top_quartile']]['event'], 
    event_observed_B=data[data['bottom_quartile']]['event']
)
plt.annotate(f'p-value: {results.p_value:.4f}', xy=(0.7, 0.8), xycoords='axes fraction')

plt.show()

# Perform Kaplan-Meier analysis for each subtype
subtypes = data['CLAUDIN_SUBTYPE'].unique()
for subtype in subtypes:
    subset = data[data['CLAUDIN_SUBTYPE'] == subtype]
    if subset.empty:
        continue
    
    fig, ax = plt.subplots()

    kmf.fit(durations=subset[subset['top_quartile']]['OS_MONTHS'], 
            event_observed=subset[subset['top_quartile']]['event'], 
            label='Top Quartile Expression')
    kmf.plot_survival_function(ax=ax)

    kmf.fit(durations=subset[subset['bottom_quartile']]['OS_MONTHS'], 
            event_observed=subset[subset['bottom_quartile']]['event'], 
            label='Bottom Quartile Expression')
    kmf.plot_survival_function(ax=ax)

    plt.title(f'Kaplan-Meier Survival Curve for {gene_expression} Expression in {subtype}')
    plt.xlabel('Months')
    plt.ylabel('Survival Probability')

    results = logrank_test(
        subset[subset['top_quartile']]['OS_MONTHS'], 
        subset[subset['bottom_quartile']]['OS_MONTHS'], 
        event_observed_A=subset[subset['top_quartile']]['event'], 
        event_observed_B=subset[subset['bottom_quartile']]['event']
    )
    plt.annotate(f'p-value: {results.p_value:.4f}', xy=(0.7, 0.8), xycoords='axes fraction')

    plt.show()
