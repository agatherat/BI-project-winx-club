import pandas as pd
import json

json_file_name='data.json'

with open(json_file_name, 'r', encoding='utf-8') as file:
    data = json.load(file)

sub_main_categories = []
def create_info_category(category_name, category_subcategories, parent_name):

    sub_main_categories.append({
        'Active (0/1)': 1,
        'Name *': category_name,
        'Parent category': parent_name
    })


    if "subcategories" in category_subcategories:
        subcategories = category_subcategories["subcategories"]
    else:
        subcategories={}
    for subcategory_name, subcategory_subcategories in subcategories.items():
        create_info_category(subcategory_name, subcategory_subcategories, category_name)


for category_name, category_subcategories in data.items():
    create_info_category(category_name, category_subcategories, "Home")

csv_data = pd.DataFrame(sub_main_categories)

csv_data.to_csv('categories_data.csv', index=False, sep=';')

