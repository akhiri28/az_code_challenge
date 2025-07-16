from modules import *


def main():

    # Common steps for questions 1 and 2
    year = 2021
    # extract_data(year)
    file_name = get_file_name(year)
    input_dir = Path("..") / "data"
    input_path = input_dir / file_name
    q_df = pd.read_csv(input_path, header = None)
    q_df = clean_data(q_df)
    postcode_area_after_cutoff = constraints(q_df, min_cutoff = 10)
    q_df = q_df.loc[q_df['postcode_area'].isin(postcode_area_after_cutoff)]

    ## Question 1 ##
    print('Working on Question 1')
    print('What are the top 10 postcode areas (for example CB22, DL4, …) with the lowest yearly median house price paid in the year 2021?')
    top_n = top_n_areas_lowest_price(q_df, 10, 'median')
    save_output('Q1.txt', top_n)


    ## Question 2 ##
    print('Working on Question 2')
    print('What are the top 5 postcode areas prefixed with CB and with the smallest yearly mean house price in the year 2021?')
    pattern = 'CB'
    pattern_match = q_df['postcode_area'].str.startswith(pattern)
    q_df = q_df.loc[pattern_match]
    top_n = top_n_areas_lowest_price(q_df, 5, 'mean')
    save_output('Q2.txt', top_n)


    ## Common Steps for Question3 and 4 ##
    # start_year = 2020
    # end_year = 2021
    # years = [y for y in range(start_year,end_year+1)]

    # df = pd.DataFrame(columns= col_names)
    # for year in years:
    #     file_path = Path("..") / "data" / f"pp-{year}.csv"
    #     df_temp = pd.read_csv(file_path, header=None, names=col_names) 
    #     df = pd.concat([df, df_temp], ignore_index = True)
    q_df = read_files_as_dataframe(input_dir)
    q_df = clean_data(q_df)
    q_df = q_df.loc[q_df['postcode_area'].isin(postcode_area_after_cutoff)]


    ## Question 3 ##
    print('Working on Question 3')
    print('What are the top overall 25 postcode areas with the lowest cumulative yearly median difference sum house price since registered by 1995 up to 2021?')
    q3_df = cumulative_yearly_metric_difference(q_df, 'median')
    intermediate_output = Path("..") / "intermediate"
    q3_df.to_csv(intermediate_output / 'q3.csv')
    top_n = q3_df.groupby('postcode_area')['price_diff'].sum().sort_values().iloc[:25].index.to_list()
    save_output('Q3.txt', top_n)
    


    ## Question 4 ##
    print('Question 4.')
    print('''
If we filter by postcode area prefix “CB”, take the top 5 smallest yearly median price postcode areas and sort them by the cumulative yearly 
mean difference sum price in ascending order, what is the result of it?
''')
    pattern = 'CB'
    pattern_match = q_df['postcode_area'].str.startswith(pattern)
    CBpostaArea_medianPrice_df = q_df.loc[pattern_match]
    top_n = top_n_areas_lowest_price(CBpostaArea_medianPrice_df, 5, 'median')
    CBpostaArea_medianPrice_df = CBpostaArea_medianPrice_df.loc[CBpostaArea_medianPrice_df['postcode_area'].isin(top_n)]
    q4_df = cumulative_yearly_metric_difference(CBpostaArea_medianPrice_df, 'mean')
    q4_df.to_csv(intermediate_output / 'q4.csv')
    top_n = q4_df.groupby('postcode_area')['price_diff'].sum().sort_values().iloc[:5].index.to_list()
    save_output('Q4.txt', top_n)



if __name__ == "__main__":
    main()

