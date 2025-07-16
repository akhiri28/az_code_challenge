import pandas as pd
import numpy as np
import requests
from pathlib import Path

col_names = ['tid', 'price', 'dateOfTransfer', 'postcode', 'propertyType', 'isNewProperty', 'tenure', 'paon', 'saon', 'street', 'locality', 'city', 'district',
             'country', 'ttype', 'recordStatus']



def create_folder_structure():

    data_dir = Path("..") / "data"
    data_dir.mkdir(parents=True, exist_ok=True)  

    results_dir = Path("..") / "results"
    results_dir.mkdir(parents=True, exist_ok=True) 

    intermediate_dir = Path("..") / "intermediate"
    intermediate_dir.mkdir(parents=True, exist_ok=True) 

def get_file_name(year):
    url = get_url(year)
    return url.split('/')[-1]

def get_url(year):

    url = f'http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-{year}.csv'

    return url

def extract_data(year):

    url = get_url(year)
    # filename = url.split('/')[-1]
    filename = get_file_name(year)

    output_dir = Path("..") / "data"
    # output_dir.mkdir(parents=True, exist_ok=True)  # Create folder if it doesn't exist
    output_path = output_dir / filename
    # output_path = f'data\{filename}'

    response = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(response.content)

    # df = pd.read_csv(url, header = None)
    print(f'Extracted data for year {year} and stored in {output_path}')
    # return df

def read_files_as_dataframe(folderpath):
    df = pd.DataFrame(columns= col_names)
    for file_path in folderpath.glob("*.csv"):  
        df_temp = pd.read_csv(file_path)
        df_temp.columns = col_names
        df = pd.concat([df, df_temp], ignore_index = True)
    return df


def clean_data(df):

    ### Cleaning Data and return only required data ###
    # Give column Names
    df.columns = col_names 
    # 1. Remove Rows with null post codes
    df = df.loc[~ df['postcode'].isnull(), ['dateOfTransfer','postcode', 'price']]
    # Handling Date
    df['dateOfTransfer'] = pd.to_datetime(df['dateOfTransfer'])
    # Derive post code area
    df['postcode_area'] = df['postcode'].apply(lambda x: x.split(' ')[0])
    # Extract Year
    df['year'] = df['dateOfTransfer'].dt.year
    print('Cleaned Data - Handled null values and date type, extracted year of transfer, postal code area')

    return df


def top_n_areas_lowest_price(data, n, metric):

    if metric == 'median':
        top_n_df = data.groupby('postcode_area')['price'].median().sort_values()

    if metric == 'mean':
        top_n_df = data.groupby('postcode_area')['price'].mean().sort_values()

    top_n_areas = top_n_df.iloc[:n].index.to_list()
    
    return top_n_areas
    

def cumulative_yearly_metric_difference(data, metric):
    
    if metric == 'median':
    
        q_df = data.groupby(['postcode_area', 'year'])['price'].median()

    if metric == 'mean':

        q_df = data.groupby(['postcode_area', 'year'])['price'].mean()
    
    q_df= q_df.reset_index(drop = False)
    q_df['price_diff'] = q_df.groupby(['postcode_area'])['price'].diff()
    q_df['price_diff']= q_df['price_diff'].fillna(0)

    return q_df

def save_output(file_name, output):

    #postcode_areas = ['DL4', 'TS1', 'BD1', 'DL17', 'SR1', 'SR8', 'DN31', 'BB11', 'TS3', 'TS29']

    output_dir = Path("..") / "results"
    # output_dir.mkdir(parents=True, exist_ok=True)  # Create folder if it doesn't exist
    output_path = output_dir / file_name

    with open(output_path, "w") as f:
        for area in output:
            f.write(area + "\n")

    print(f"Saved to results in results\{file_name}")


def constraints(data, min_cutoff):

    counts_series = data['postcode_area'].value_counts()
    postcode_areas_cutoff = counts_series[counts_series >= min_cutoff].index.to_list()

    return postcode_areas_cutoff






# import requests
# from pathlib import Path

# def main():
#     # url = "https://example.com/data.csv"
#     # folder = Path("downloads")
#     # folder.mkdir(exist_ok=True)

#     # output_file = folder / "data.csv"

#     # with requests.get(url, stream=True) as r:
#     #     r.raise_for_status()
#     #     with open(output_file, "wb") as f:
#     #         for chunk in r.iter_content(chunk_size=8192):
#     #             f.write(chunk)

#     # print(f"File saved to {output_file}")
#     print('create folder structure')
#     create_folder_structure()

#     # print('Working on Question 1')
#     # print('What are the top 10 postcode areas (for example CB22, DL4, …) with the lowest yearly median house price paid in the year 2021?')
#     # year = 2021
#     # extract_data(year)
#     # file_name = get_file_name(year)
#     input_dir = Path("..") / "data"
#     # # output_dir.mkdir(parents=True, exist_ok=True)  # Create folder if it doesn't exist
#     # input_path = input_dir / file_name
#     # q_df = pd.read_csv(input_path, header = None)
#     # q_df = clean_data(q_df)

#     # top_n = top_n_areas_lowest_price_inYear(q_df, 10, 'median')
#     # save_output('Q1.txt', top_n)

#     # print('Working on Question 2')
#     # print('What are the top 5 postcode areas prefixed with CB and with the smallest yearly mean house price in the year 2021?')
#     # # q_df = extract_data(2021)
#     # # q_df = clean_data(q_df)
#     # pattern = 'CB'
#     # pattern_match = q_df['postcode_area'].str.startswith(pattern)
#     # q_df = q_df.loc[pattern_match]
#     # top_n = top_n_areas_lowest_price_inYear(q_df, 5, 'mean')
#     # save_output('Q2.txt', top_n)

#     print('Working on Question 3')
#     print('What are the top overall 25 postcode areas with the lowest cumulative yearly median difference sum house price since registered by 1995 up to 2021?')
#     # start_year = 2015
#     # end_year = 2021
#     # years = [y for y in range(start_year,end_year+1)]

#     # # df = pd.DataFrame(columns= col_names)
#     # for year in years:
#     #     print(year)
#     #     extract_data(year)
#     #     # df_temp = pd.read_csv(f'E:\learn\interview\data\pp-{year}.csv', header = None,  names = col_names)
#     #     # df = pd.concat([df, df_temp], ignore_index = True)
#     #     # print(df.shape)
#     q_df = read_files_as_dataframe(input_dir)
#     print(q_df.shape)
#     print(q_df.columns)
#     q_df = clean_data(q_df)
#     q3_df = cumulative_yearly_metric_difference(q_df, 'median')
#     top_n = q3_df.groupby('postcode_area')['price_diff'].sum().sort_values().iloc[:25].index.to_list()
#     print(top_n)
#     save_output('Q3.txt', top_n)
    
#     print('Question 4.')
#     print('''
# If we filter by postcode area prefix “CB”, take the top 5 smallest yearly median price postcode areas and sort them by the cumulative yearly 
# mean difference sum price in ascending order, what is the result of it?
# ''')
#     pattern = 'CB'
#     pattern_match = q_df['postcode_area'].str.startswith(pattern)
#     CBpostaArea_medianPrice_df = q_df.loc[pattern_match]
#     top_n = top_n_areas_lowest_price_inYear(CBpostaArea_medianPrice_df, 5, 'median')
#     CBpostaArea_medianPrice_df = CBpostaArea_medianPrice_df.loc[CBpostaArea_medianPrice_df['postcode_area'].isin(top_n)]
#     q4_df = cumulative_yearly_metric_difference(CBpostaArea_medianPrice_df, 'mean')
#     top_n = q4_df.groupby('postcode_area')['price_diff'].sum().sort_values().iloc[:5].index.to_list()
#     print(top_n)
#     save_output('Q4.txt', top_n)

# if __name__ == "__main__":
#     main()

