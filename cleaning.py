#data cleaning

import pandas as pd
import os

def read_and_clean_data(files, columns_indices,row_names,start_idx,end_idx):

      
  # Initialize a dictionary to store DataFrames for each index
    dfs_by_idx = {idx: pd.DataFrame() for idx in columns_indices}

  # Process each file, adding column to diff df each
    for file in files:
        try:
            # Open the Excel file and parse the first sheet
            excel_data = pd.ExcelFile(file)
            temp_df = excel_data.parse(excel_data.sheet_names[0])

            # Clean the DataFrame: Remove the first  rows and last rows
            temp_df = temp_df.iloc[start_idx:end_idx]

            # Reset the index to be just 0,1 etc
            temp_df.reset_index(drop=True, inplace=True)

            # Process each column index into correct df
            for idx in columns_indices:
                if idx < temp_df.shape[1]:  #Ensure the column exists
                    col_data = temp_df.iloc[:, [idx]].copy()
                    col_data.rename(columns={col_data.columns[0]: os.path.splitext(file)[0]}, inplace=True)#renames col name of file

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
    return dfs_by_idx