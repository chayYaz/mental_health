from correlation_analysis import process_and_analyze_dataframe
from cleaning import read_and_clean_data
from visualization import plot2
row_names = ["diffrences by SEX","Men","Women","diffrences by AGE","20-44","45-64","65-74","75+","diffrences by MARITAL STATUS","Married","Divorced","Widowed","Never married","diffrences by POPULATION GROUP","Jews and others","Jews","Arabs","IMMIGRANTS OF 1990 OR LATER","EXTENT OF RELIGIOSITY - JEWS","Ultra-Orthodox","Religious jews","Traditional jews","Not religious, secular jews","EXTENT OF RELIGIOSITY - OTHER RELIGIONS","Very religious and religious non-jews","Not-so-religious and not religious non-jews","diffrences by HIGHEST DIPLOMA RECEIVED","diffrences by education level","diffrences by education level Thereof: ","Primary or lower secondary school diploma, or no diploma","Upper secondary school diploma (no matriculation certificate)","      Matriculation certificate ","Short-cycle tertiary school diploma (not academic track)","Academic degree","diffrences by LABOUR FORCE CHARACTERISTICS","Employed","Unemployed and not in labour force","AVERAGE HOUSEHOLD INCOME PER CAPITA","Income per person (GROSS MONTHLY) - NIS","Up to 2,000","2,001-4,000","Over 4,000","SATISFACTION WITH LIFE","SATISFACTION WITH LIFE Very satisfied or satisfied","SATISFACTION WITH LIFE Not so satisfied or not satisfied at all","SATISFACTION WITH ECONOMIC SITUATION","SATISFACTION WITH ECONOMIC SITUATION Very satisfied or satisfied","SATISFACTION WITH ECONOMIC SITUATION Not so satisfied or not satisfied at all","SELF-ASSESSED HEALTH","SELF-ASSESSED HEALTH Very good or good","SELF-ASSESSED HEALTH Not so good or not good at all"]

files = ['2023.xlsx', '2022.xlsx', '2021.xls', '2020.xls', '2019.xls', '2018.xls']
files.reverse()
columns_indices = [1, 2, 3, 4, 5]

dfs_by_idx = read_and_clean_data(files, columns_indices,row_names,9,60)
print("dfs_by_idx",dfs_by_idx)
depressed_df = dfs_by_idx[1].fillna(0)
problems_df = dfs_by_idx[2].fillna(0)
disturbed_sleep_df = dfs_by_idx[3].fillna(0)
energetic_df = dfs_by_idx[4].fillna(0)
stressed_df = dfs_by_idx[5].fillna(0)



dataframes_with_names = [
    ("depressed_df", depressed_df),
    ("problems_df", problems_df),
    ("disturbed_sleep_df", disturbed_sleep_df),
    ("energetic_df", energetic_df),
    ("stressed_df", stressed_df)
]

for df_name, df in dataframes_with_names:
    # Call the function with the DataFrame and its name
  print("hello")
  sorted_correlations = process_and_analyze_dataframe(df, top_n=5,df_name=df_name)
  
# Access the most correlated rows
  print(sorted_correlations.head())
disturbed_sleep_df.index = disturbed_sleep_df.index.astype(str)
# Assuming 'disturbed_sleep_df' is a DataFrame from data_cleaning.py
plot2(disturbed_sleep_df, 'Unemployed', 'Up to 2,000',"Disturbed Sleep",col_subject="year")
