import plotly.express as px
import pandas as pd

# Example data
df = pd.read_excel("Overall_survival.xlsx", sheet_name="LumA_NSD1_TCGA")

# Plot
fig = px.line(df, x='Time.months', y='Survival', color='Group')
fig.show()
