import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

def load_data(filepath):
    return pd.read_csv(filepath)

def ensure_columns_present(data, required_columns):
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"Missing one or more required columns: {required_columns}")

def convert_os_status(data):
    data['event'] = data['OS_STATUS'].apply(lambda x: 1 if x == '1:DECEASED' else 0)
    return data

def limit_months(data, max_months):
    return data[data['OS_MONTHS'] <= max_months]

def create_expression_groups(data, gene_expression, option):
    if option == 1:
        data['high_expression'] = data[gene_expression] > data[gene_expression].median()
    elif option == 2:
        top_quartile_threshold = data[gene_expression].quantile(0.75)
        bottom_quartile_threshold = data[gene_expression].quantile(0.25)
        data['high_expression'] = data[gene_expression] >= top_quartile_threshold
        data['low_expression'] = data[gene_expression] <= bottom_quartile_threshold
    else:
        raise ValueError("Option must be 1 (median) or 2 (top and bottom quartiles)")
    return data

def plot_kaplan_meier(data, gene_expression, option, title_suffix="(Entire Cohort)"):
    kmf = KaplanMeierFitter()
    fig, ax = plt.subplots()

    if option == 1:
        kmf.fit(durations=data[data['high_expression']]['OS_MONTHS'], 
                event_observed=data[data['high_expression']]['event'], 
                label='High Expression')
        kmf.plot_survival_function(ax=ax)

        kmf.fit(durations=data[~data['high_expression']]['OS_MONTHS'], 
                event_observed=data[~data['high_expression']]['event'], 
                label='Low Expression')
        kmf.plot_survival_function(ax=ax)

        results = logrank_test(
            data[data['high_expression']]['OS_MONTHS'], 
            data[~data['high_expression']]['OS_MONTHS'], 
            event_observed_A=data[data['high_expression']]['event'], 
            event_observed_B=data[~data['high_expression']]['event']
        )
    elif option == 2:
        kmf.fit(durations=data[data['high_expression']]['OS_MONTHS'], 
                event_observed=data[data['high_expression']]['event'], 
                label='Top Quartile Expression')
        kmf.plot_survival_function(ax=ax)

        kmf.fit(durations=data[data['low_expression']]['OS_MONTHS'], 
                event_observed=data[data['low_expression']]['event'], 
                label='Bottom Quartile Expression')
        kmf.plot_survival_function(ax=ax)

        results = logrank_test(
            data[data['high_expression']]['OS_MONTHS'], 
            data[data['low_expression']]['OS_MONTHS'], 
            event_observed_A=data[data['high_expression']]['event'], 
            event_observed_B=data[data['low_expression']]['event']
        )

    plt.title(f'Kaplan-Meier Survival Curve for {gene_expression} Expression {title_suffix}')
    plt.xlabel('Months')
    plt.ylabel('Survival Probability')
    plt.annotate(f'p-value: {results.p_value:.4f}', xy=(0.7, 0.8), xycoords='axes fraction')
    plt.show()

def plot_kaplan_meier_by_subtype(data, gene_expression, option):
    subtypes = data['CLAUDIN_SUBTYPE'].unique()
    for subtype in subtypes:
        subset = data[data['CLAUDIN_SUBTYPE'] == subtype]
        if subset.empty:
            continue

        kmf = KaplanMeierFitter()
        fig, ax = plt.subplots()

        if option == 1:
            kmf.fit(durations=subset[subset['high_expression']]['OS_MONTHS'], 
                    event_observed=subset[subset['high_expression']]['event'], 
                    label='High Expression')
            kmf.plot_survival_function(ax=ax)

            kmf.fit(durations=subset[~subset['high_expression']]['OS_MONTHS'], 
                    event_observed=subset[~subset['high_expression']]['event'], 
                    label='Low Expression')
            kmf.plot_survival_function(ax=ax)

            results = logrank_test(
                subset[subset['high_expression']]['OS_MONTHS'], 
                subset[~subset['high_expression']]['OS_MONTHS'], 
                event_observed_A=subset[subset['high_expression']]['event'], 
                event_observed_B=subset[~subset['high_expression']]['event']
            )
        elif option == 2:
            kmf.fit(durations=subset[subset['high_expression']]['OS_MONTHS'], 
                    event_observed=subset[subset['high_expression']]['event'], 
                    label='Top Quartile Expression')
            kmf.plot_survival_function(ax=ax)

            kmf.fit(durations=subset[subset['low_expression']]['OS_MONTHS'], 
                    event_observed=subset[subset['low_expression']]['event'], 
                    label='Bottom Quartile Expression')
            kmf.plot_survival_function(ax=ax)

            results = logrank_test(
                subset[subset['high_expression']]['OS_MONTHS'], 
                subset[subset['low_expression']]['OS_MONTHS'], 
                event_observed_A=subset[subset['high_expression']]['event'], 
                event_observed_B=subset[subset['low_expression']]['event']
            )

        plt.title(f'Kaplan-Meier Survival Curve for {gene_expression} Expression in {subtype}')
        plt.xlabel('Months')
        plt.ylabel('Survival Probability')
        plt.annotate(f'p-value: {results.p_value:.4f}', xy=(0.7, 0.8), xycoords='axes fraction')
        plt.show()

def main():
    filepath = 'cleaned_clinical_nsd1_data.csv'
    data = load_data(filepath)

    required_columns = ['OS_MONTHS', 'OS_STATUS', 'CLAUDIN_SUBTYPE', 'NSD1']
    ensure_columns_present(data, required_columns)

    data = convert_os_status(data)
    data = limit_months(data, 200)

    option = int(input("Press 1 to compare based on median; Press 2 to compare top to bottom quartile: "))
    data = create_expression_groups(data, 'NSD1', option)

    plot_kaplan_meier(data, 'NSD1', option)
    plot_kaplan_meier_by_subtype(data, 'NSD1', option)

if __name__ == "__main__":
    main()
