"""
This is a simple that expects that the data in p_i,json form is stored in a local directory.
And cleans and formats the data, and then converts it to a CSV and excel file for easy use.
"""

import json
import os
from typing import Tuple

import pandas as pd
from tqdm import tqdm


def clean_name(fn: str) -> Tuple[str, str]:
    prefix = ["Ms", "MS", "Mrs", "MRS", "Mr", "MR", "DR", "Dr", "Prof", "Ms.", "MS.", "Mrs.", "MRS.", "Mr.", "MR.",
              "DR.", "Dr.", "Prof.", "Miss", "Miss.", "Professor", "Professor."]
    prefix_lower = [s.lower() for s in prefix]
    split_name = fn.split(" ")
    name_sp = []

    for k in split_name:
        k = k.replace(",", "").replace(".", "")
        if k not in prefix and k.lower() not in prefix_lower and len(k) >= 1:
            name_sp.append(k)

    first_name = name_sp[0].strip() if name_sp else None
    if len(name_sp) > 2:
        last_name = name_sp[1].strip() if len(name_sp[1].strip()) > 2 else name_sp[2].strip()
    elif len(name_sp) > 1:
        last_name = name_sp[1].strip()
    else:
        last_name = None

    return first_name, last_name


if __name__ == '__main__':
    max_expected = 13000  # max expected pages. Could be done many other ways without it
    output_prefix = "GPs"  # prefix for output file
    directory = "output2/"  # directory in which data resides

    files = os.listdir(directory)
    data_arr = [None] * (max_expected + 1)

    for file in files:
        with open(os.path.join(directory, file), "r") as f:
            data = json.load(f)

        page = data["page"]
        scraped_data = data["data"]

        data_arr[page] = scraped_data

    filtered_data_arr = [d for d in data_arr if d]

    formatted_data = []
    data_list: list
    for data_list in tqdm(filtered_data_arr):
        for dic in data_list:
            full_name = dic["full_name"]
            firstname, lastname = clean_name(full_name)

            obj = {
                "full_name": full_name,
                "first_name": firstname,
                "last_name": lastname,
                "speciality": dic.get("speciality"),
                "hospital_name": dic.get("hospital_name"),
                "hospital_postcode": dic.get("hospital_postcode")
            }

            formatted_data.append(obj)

    print("Starting Saving ...")
    df2 = pd.DataFrame(formatted_data)
    df2.to_csv(f"data/{output_prefix}_formatted_data.csv")
    df2.to_excel(f"data/{output_prefix}_formatted_data.xlsx")
    print("Data Saved.")
