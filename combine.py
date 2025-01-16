import pandas as pd
import os
import matplotlib.pyplot as plt
import inspect
# רשימה של שמות הקבצים (קובצי Excel)
files = ['2023.xlsx', '2022.xlsx','2021.xls','2020.xls', '2019.xls','2018.xls']  # החליפי בשמות הקבצים שלך
files.reverse()
columns_indices = [0, 1, 2, 3, 4, 5]

row_names = ["diffrences by SEX","Men","Women","diffrences by AGE","20-44","45-64","65-74","75+","diffrences by MARITAL STATUS","Married","Divorced","Widowed","Never married","diffrences by POPULATION GROUP","Jews and others","Jews","Arabs","IMMIGRANTS OF 1990 OR LATER","EXTENT OF RELIGIOSITY - JEWS","Ultra-Orthodox","Religious jews","Traditional jews","Not religious, secular jews","EXTENT OF RELIGIOSITY - OTHER RELIGIONS","Very religious and religious non-jews","Not-so-religious and not religious non-jews","diffrences by HIGHEST DIPLOMA RECEIVED","diffrences by education level","diffrences by education level Thereof: ","Primary or lower secondary school diploma, or no diploma","Upper secondary school diploma (no matriculation certificate)","      Matriculation certificate ","Short-cycle tertiary school diploma (not academic track)","Academic degree","diffrences by LABOUR FORCE CHARACTERISTICS","Employed","Unemployed and not in labour force","AVERAGE HOUSEHOLD INCOME PER CAPITA","Income per person (GROSS MONTHLY) - NIS","Up to 2,000","2,001-4,000","Over 4,000","SATISFACTION WITH LIFE","SATISFACTION WITH LIFE Very satisfied or satisfied","SATISFACTION WITH LIFE Not so satisfied or not satisfied at all","SATISFACTION WITH ECONOMIC SITUATION","SATISFACTION WITH ECONOMIC SITUATION Very satisfied or satisfied","SATISFACTION WITH ECONOMIC SITUATION Not so satisfied or not satisfied at all","SELF-ASSESSED HEALTH","SELF-ASSESSED HEALTH Very good or good","SELF-ASSESSED HEALTH Not so good or not good at all"]


# Initialize a dictionary to store DataFrames for each index
dfs_by_idx = {idx: pd.DataFrame() for idx in columns_indices}

# Process each file
for file in files:
    try:
        # Open the Excel file and parse the first sheet
        excel_data = pd.ExcelFile(file)
        temp_df = excel_data.parse(excel_data.sheet_names[0])

        # Clean the DataFrame: Remove the first 10 rows and last 9 rows
        temp_df = temp_df.iloc[9:60]

        # Reset the index if not already present
        temp_df.reset_index(drop=True, inplace=True)

        # Process each column index
        for idx in columns_indices:
            if idx < temp_df.shape[1]:  # Ensure the column exists
                col_data = temp_df.iloc[:, [idx]].copy()
                col_data.rename(columns={col_data.columns[0]: os.path.splitext(file)[0]}, inplace=True)

                # Merge data into the main DataFrame for the column index
                if dfs_by_idx[idx].empty:
                    dfs_by_idx[idx] = col_data
                else:
                    dfs_by_idx[idx] = pd.merge(
                        dfs_by_idx[idx], col_data, left_index=True, right_index=True, how='outer'
                    )

    except Exception as e:
        print(f"Error processing file {file}: {e}")


# Assign row names (only if row count matches)
expected_row_count = len(row_names)
for idx, df in dfs_by_idx.items():
    if len(df) == expected_row_count:
        df.index = pd.Index(row_names)
    else:
        print(f"Warning: DataFrame for index {idx} has row count {len(df)} (expected {expected_row_count}).")
    for col in df.columns:#???
      df[col] = pd.to_numeric(df[col], errors='coerce')

# Extract specific DataFrames
depressed_df = dfs_by_idx[1].fillna(0)
problems_df = dfs_by_idx[2].fillna(0)
disturbed_sleep_df = dfs_by_idx[3].fillna(0)
energetic_df = dfs_by_idx[4].fillna(0)
stressed_df = dfs_by_idx[5].fillna(0)
import pandas as pd
import matplotlib.pyplot as plt

def process_and_analyze_dataframe(df, top_n=5, verbose=True,df_name="df"):
    """
    """
    # Ensure numeric columns
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



dataframes_with_names = [
    ("depressed_df", depressed_df),
    ("problems_df", problems_df),
    ("disturbed_sleep_df", disturbed_sleep_df),
    ("energetic_df", energetic_df),
    ("stressed_df", stressed_df)
]

for df_name, df in dataframes_with_names:
    # Call the function with the DataFrame and its name

  sorted_correlations = process_and_analyze_dataframe(df, top_n=5, verbose=True,df_name=df_name)
  
# Access the most correlated rows
  print(sorted_correlations.head())




import matplotlib.pyplot as plt

# Assuming disturbed_sleep_df is your DataFrame

# Filter the DataFrame for rows containing 'Unemployed' and 'Low Income per Capita' in the row index
unemployed_data = disturbed_sleep_df[disturbed_sleep_df.index.str.contains('Unemployed', case=False, na=False)]

low_income_data = disturbed_sleep_df[disturbed_sleep_df.index.str.contains('Up to 2,000', case=False, na=False)]

# Create two subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot for Unemployed Data
axes[0].plot(unemployed_data.columns, unemployed_data.iloc[0], label='Unemployed')
axes[0].set_title('Disturbed Sleep in Unemployed')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Disturbed Sleep Level')
axes[0].legend()

# Plot for Low Income Data
axes[1].plot(low_income_data.columns, low_income_data.iloc[0], label='Low Income', color='orange')
axes[1].set_title('Disturbed Sleep in Low Income Individuals')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Disturbed Sleep Level')
axes[1].legend()

# Display the plots
plt.tight_layout()
plt.show()
