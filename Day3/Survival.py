import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test
import plotly.graph_objects as go

# Correct Windows file path using raw string
file_path = r"Overall_survival.xlsx"

# Read the data
survdat = pd.read_excel(file_path, sheet_name="LumA_NSD1_TCGA")

# Convert 'Group' to a categorical variable
survdat['Group'] = survdat['Group'].astype('category')

# Capping 'Time.months' at 200 and updating 'censor' accordingly
survdat.loc[survdat['Time.months'] > 200, 'Time.months'] = 200
survdat.loc[survdat['Time.months'] == 200, 'censor'] = 0

# Fit the Cox Proportional Hazards model
cph = CoxPHFitter()
cph.fit(survdat[['Time.months', 'censor', 'Group']], duration_col='Time.months', event_col='censor', formula="Group")

# Compute p-value using multivariate_logrank_test
results = multivariate_logrank_test(survdat['Time.months'], survdat['Group'], survdat['censor'])
p_value = results.p_value

# Plotting the survival curves using Kaplan-Meier estimator with Plotly
kmf = KaplanMeierFitter()

# Define custom colors for the groups
colors = ['blue', 'red']

# Create the Plotly figure
fig = go.Figure()

# Plot by group using observed=True in groupby to handle categorical data efficiently
for i, (name, grouped_df) in enumerate(survdat.groupby('Group', observed=True)):
    kmf.fit(grouped_df["Time.months"], event_observed=grouped_df["censor"], label=str(name))
    km_curve = kmf.survival_function_

    fig.add_trace(go.Scatter(
        x=km_curve.index,
        y=km_curve[name],
        mode='lines',
        name=str(name),
        line=dict(color=colors[i])
    ))

# Customize the layout
fig.update_layout(
    xaxis_title="Time (Months)",
    yaxis_title="Survival Probability",
    title=dict(text="Survival Analysis", x=0.5),
    legend_title_text=f"Log-Rank p-value={p_value:.3f}",
    xaxis=dict(tickmode='linear', dtick=20),
    yaxis=dict(range=[0, 1]),
    template='plotly_white'
)

# Show the plot
fig.show()
