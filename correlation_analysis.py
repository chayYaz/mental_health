#correlation analysis

import pandas as pd
import matplotlib.pyplot as plt
def process_and_analyze_dataframe(df, top_n=5, verbose=True,df_name="df"):
    df = df.fillna(0)  # Replace NaNs with 0
    numerical_df = df.select_dtypes(include='number')
    
    # Convert column names to numeric (assumes they represent years)
    numerical_columns = pd.to_numeric(numerical_df.columns, errors='coerce')
    
    # Check for NaNs in column names after conversion
    if numerical_columns.isnull().any():
        print("Warning: Some column names could not be converted to numeric.")
    
    correlations_with_columns = []

    # Loop over each row and compute correlation with column indices
    for idx, row in numerical_df.iterrows():
        row_series = pd.Series(row.values, index=numerical_columns)
        correlation = row_series.corr(pd.Series(numerical_columns, index=numerical_columns))
        correlations_with_columns.append(abs(correlation))  # Use absolute correlation
        
        # if verbose:
        #     print(f"Row idx data: {row.values}")
        #     print(f"Numerical columns: {numerical_columns.values}")
        #     print(f"Correlation: {correlation}")
    
    # Convert correlations into a pandas Series
    correlations_with_columns = pd.Series(correlations_with_columns, index=numerical_df.index)

    # Sort correlations by absolute value in descending order
    sorted_correlations = correlations_with_columns.sort_values(ascending=False)

    # Output the most correlated rows
    if verbose:
        print("Most correlated rows with the column indices (years):")
        print(sorted_correlations.head(top_n))

    # Plot the rows with the highest correlations
    plt.figure(figsize=(10, 6))
    for idx in sorted_correlations.index[:top_n]:
        plt.plot(numerical_df.columns, numerical_df.loc[idx], label=f'Row {idx} (Correlation: {sorted_correlations[idx]:.2f})')
    





    plt.xlabel('Year')
    plt.ylabel('Values')

    
    plt.title(f'Top Rows by Correlation with Column Indices ({df_name})')
    plt.legend()
    plt.show()

    return sorted_correlations
