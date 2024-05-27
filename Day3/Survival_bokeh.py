import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import logrank_test
from bokeh.plotting import figure, show, output_file
from bokeh.models import Legend, Label
from bokeh.io import output_notebook
import sys

# Enable Bokeh to display plots in the notebook
if 'ipykernel' in sys.modules:
    output_notebook()

# Correct Windows file path using raw string
file_path = "Overall_survival.xlsx"

# Read the data
survdat = pd.read_excel(file_path, sheet_name="LumA_NSD1_TCGA")

# Convert 'Group' to a categorical variable
survdat['Group'] = survdat['Group'].astype('category')

# Ensure 'Group' contains only two groups for logrank_test
if len(survdat['Group'].unique()) != 2:
    raise ValueError("The 'Group' column must contain exactly two unique values for the logrank test.")

# Capping 'Time.months' at 200 and updating 'censor' accordingly
survdat.loc[survdat['Time.months'] > 200, 'Time.months'] = 200
survdat.loc[survdat['Time.months'] == 200, 'censor'] = 0

# Fit the Cox Proportional Hazards model
cph = CoxPHFitter()
cph.fit(survdat[['Time.months', 'censor', 'Group']], duration_col='Time.months', event_col='censor', formula="Group")

# Compute p-value using logrank_test
group1 = survdat[survdat['Group'] == survdat['Group'].unique()[0]]
group2 = survdat[survdat['Group'] == survdat['Group'].unique()[1]]

results = logrank_test(group1['Time.months'], group2['Time.months'], event_observed_A=group1['censor'], event_observed_B=group2['censor'])
p_value = results.p_value

# Plotting the survival curves using Kaplan-Meier estimator
kmf = KaplanMeierFitter()

# Create a Bokeh figure
p = figure(title="Survival Analysis", x_axis_label="Time (Months)", y_axis_label="Survival Probability", y_range=(0, 1), x_range=(0, 200))

# Colors for the groups
colors = ['blue', 'red']
legends = []

# Plot by group
for i, (name, grouped_df) in enumerate(survdat.groupby('Group', observed=False)):
    kmf.fit(grouped_df["Time.months"], event_observed=grouped_df["censor"], label=str(name))
    surv_prob = kmf.survival_function_
    line = p.line(surv_prob.index, surv_prob.values.flatten(), line_width=2, color=colors[i])
    legends.append((str(name), [line]))

# Create legend
legend = Legend(items=legends, location="center")
p.add_layout(legend, 'right')

# Add p-value annotation
label = Label(x=10, y=0.1, text="Log-Rank p-value={:.3f}".format(p_value), background_fill_color='white', background_fill_alpha=0.6)
p.add_layout(label)

# Save the plot to an HTML file if not in a notebook
if 'ipykernel' not in sys.modules:
    output_file("survival_analysis.html")

# Display the plot
show(p)
