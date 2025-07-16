from modules import *

def main():

    # folder = Path("data")
    # folder.mkdir(exist_ok=True)

    # output_file = folder / "data.csv"

    # with requests.get(url, stream=True) as r:
    #     r.raise_for_status()
    #     with open(output_file, "wb") as f:
    #         for chunk in r.iter_content(chunk_size=8192):
    #             f.write(chunk)

    # print(f"File saved to {output_file}")

    print('create folder structure')
    create_folder_structure()

    # Data Extraction ##
    print('Extracting data from URL')
    start_year = 1995
    end_year = 2021
    years = [y for y in range(start_year,end_year+1)]

    for year in years:
        extract_data(year)

if __name__ == "__main__":
    main()

