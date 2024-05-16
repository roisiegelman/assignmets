import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Correct Windows file path using raw string
file_path = "Overall_survival.xlsx"

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

# Plotting the survival curves using Kaplan-Meier estimator
kmf = KaplanMeierFitter()

ax = plt.subplot(111)

# Plot by group
for name, grouped_df in survdat.groupby('Group'):
    kmf.fit(grouped_df["Time.months"], event_observed=grouped_df["censor"], label=str(name))
    kmf.plot_survival_function(ax=ax, ci_show=False)

ax.set_xlim(0, 200)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_ylim(0, 1)
ax.set_xlabel("Time (Months)")
ax.set_ylabel("Survival Probability")

# Add legend with p-value
plt.legend(title="Log-Rank p-Value={:.3f}".format(p_value), loc="upper right")

# Customizing the plot aesthetics
ax.title.set_text('Survival Analysis')
plt.show()
