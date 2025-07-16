
__Note - Extracting file take more than 30 mins as each csv file is from 150 - 200 MB__
__I am have extracted all files at once as Q3 and Q4 needs all files where are Q1 and Q2 need only 2021 file__


__Question 1__:
What are the top 10 postcode areas (for example CB22, DL4, …) with the lowest yearly median house price paid in the year 2021?

__Question 2__:
What are the top 5 postcode areas prefixed with CB and with the smallest yearly mean house price in the year 2021?

__Question 3__:
What are the top overall 25 postcode areas with the lowest cumulative yearly median difference sum house price since registered by 1995 up to 2021?

__Question 4__:
If we filter by postcode area prefix “CB”, take the top 5 smallest yearly median price postcode areas and sort them by the cumulative yearly mean difference sum price in ascending order, what is the result of it?

__Constraints__:
From the result of each question, you must drop any entry with an aggregated yearly number of transactions less or equal to 10 in 2021.

__Folder Straucture__
- Interview
   - data
   - results
   - src
   - intermediate

- __data__ - This folder has data extracted from the URL. It is the output of extraction step.
- __results__ - This folder has the answers to the question listed above step.
- __src__ - This folder has 3 python files. extraction.py, modules.py and transformation.py.
- __intermediate__ - This folder has some intermediate transformation date.


- __How to run the script__
- clone the repo -> open the vscode from the fodler -> open terminal -> navigate to src folder -> run the command 'python extraction.py' -> run the command 'python transformation.py'

- __python extraction.py__ - creates two folders data and results. Extracts data and stores it in the data folder.
- __python transformation.py__ - answers all the questions [1 to 4] and stores the text files in results folder.


__modules.py__ - python file has function to perform modular tasks.
1. create_folder_structure() - Create data and results folder.
2. get_file_name(year) - creates the file name that has to be extracted using URL. It takes year as input and outputs file name. 
3. get_url(year) - Creates URL used to extract the data. It takes year as input. It takes year as input and output is a URL of type string.
4. extract_data(year) - Extract the data using URL. It takes year as input. Uses get_file_name and get_url functions and extracts data and stores in data folder.
5. read_files_as_dataframe(input_dir) - Read all the files from data folder in the memory as concatenated dataframe.
6. clean_data(df) - Cleans data, handles null values, date types, extract year, strings. Return a cleaned dataframe.
7. top_n_areas_lowest_price(data, n, metric) - It finds out top n postcode areas with lowest metric. Metric may be median or mean. It takes dataframe, metric and n as inputs and outputs top n postcode areas as list.
8. cumulative_yearly_metric_difference(data, metric) - Finds first difference of the metric (median or mean) on price grouped by postcode area and year. Output is a dataframe with metric of price and its first diffrentiation.
9. save_output(file_name, output) - Saves output to the results folder. Output is in text format.
10. constraints(data, min_cutoff) - Applies contraints or conditions on the task. [From the result of each question, you must drop any entry with an aggregated yearly number of transactions less or equal to 10 in 2021.]

__extraction.py__ - python files to extract the data. 
1. It creates two folders if not existent. 
2. It extracts data from URL and stores in data folder.

__transformation.py__ - python file to generate output. 
1. Reads data from data folder.
Common for  question 1 and 2 [2,3,4]
2. For question 1 and question 2 it reads data only for year 2021.
3. Cleans data to handle null values in postcode, date type, extracts year from date and split postcode to extract postcode area.
4. Applies constraint as mentioned in step 10 under modules.
For Question 1 [5]
5. Uses, top_n_areas_lowest_price function to get the top 10 lowest median price for the year 2021 and postcode area.
For Question 2 [6]
6. Filter the data to select only the postcode areas starting with 'CB'. Uses, top_n_areas_lowest_price function to get the top 5 lowest mean price for the year 2021 and postcode area.
Common steps for Question 3 and 4 [7,8,9]
7. Reads all the csv files from data folder, concates all the data into one dataframe.
8. Cleans the dataframe similar to step 3 under transformation.
9. Applies constraint as mentioned in step 10 under modules.
For Question 3 [10,11]
10. For each postcode area and year between 1995 and 2021, get median on price and first difference  (price_diff) of the same metric.
11. Sum up the first difference of median on price (price_diff) for each postcode area. Order it based on the sum in ascending order and select the top 25.
For Question 4 [12]
12. Filter the data (from 1995 to 2021) to select only the postcode areas starting with 'CB'.
13. Uses, top_n_areas_lowest_price function to get the top 5 postcode area with lowest median price.
14. Filter data with from step 12 using the post code area found in step 13.
15. Use data from step 14, get mean on price and first difference  (price_diff) on the mean on price.
16. Sum up the first difference of mean on price (price_diff) for each postcode area. Order it based on the sum in ascending order and select the top 5.
17. Ouput is the ordered postcode area from step 16.



data_extract.ipynb - file used for experimentation.
