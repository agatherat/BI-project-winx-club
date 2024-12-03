import json
import pandas as pd

with open('products.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

products_info = []
vat_tax=23 # w procentach

def save_product(product_name, product_url,category_path,product_description,product_price_after_tax,product_quantity,product_image):
    number_price_after_tax = product_price_after_tax.replace("zł", "").strip()
    number_price_after_tax = number_price_after_tax.replace(",", ".")
    price_after_tax_float = float(number_price_after_tax)
    price_before_tax=price_after_tax_float / (1 + (vat_tax / 100))
    price_before_tax=round(price_before_tax, 2)
    if product_quantity == "Out of stock" or product_quantity=="Brak w magazynie":
        quantity_number = 0
    else:
        quantity_number = int(product_quantity.split()[0])
    tax_rule_id=1

    if not any(prod['URL'] == product_url for prod in products_info):
        products_info.append({
            'Name': product_name,
            'Category': category_path,
            'URL': product_url,
            'Description':product_description,
            'Price before tax': price_before_tax,
            'Tax Rule ID':tax_rule_id,
            'Quantity':quantity_number,
            'Image':product_image
        })

def create_info_category(category_name, category_data, parent_category_path):
    if parent_category_path:
        current_category_path = f"{parent_category_path}/{category_name}"
    else:
        current_category_path = category_name

    if "subcategories" in category_data:
        subcategories = category_data["subcategories"]
        for subcategory_name, subcategory_data in subcategories.items():
            create_info_category(subcategory_name, subcategory_data, current_category_path)

    if "products" in category_data:
        for product in category_data["products"]:
            save_product(product["name"],product["url"], current_category_path,product['description'],product['price'],product['stock'],product['image'])

for category_name, category_data in data.items():
    create_info_category(category_name, category_data, "")

csv_data = pd.DataFrame(products_info)

if 'URL' in csv_data.columns:
    csv_data = csv_data.drop(columns=['URL'])

csv_data.to_csv('insert_products.csv', index=False, sep=';')

