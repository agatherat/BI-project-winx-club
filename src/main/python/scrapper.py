from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import json
import os

def getSubcategories(kategoria,categoryLink):
    urlSubcategories = categoryLink
    pageSubCategories=urlopen(urlSubcategories)
    html_bytes_subcategories = pageSubCategories.read()
    html_subcategories = html_bytes_subcategories.decode("utf-8")
    soup=BeautifulSoup(html_subcategories, "html.parser")
    subcategories_dic={}
    parent_category=None
    #znajdujemy wszystkie elementy <li class="cat-parent"> czyli rodzic
    all_possible_parent_categories=soup.find_all('li', class_='cat-parent')
    #iterujemy przez wszystkie mozliwe gdy dotrzemy do interersujacego nas rodzica kategori i wychodzimy z petli
    for main_category in all_possible_parent_categories:
        # znajdujemy pierwszy tag <a> w bieżącym elemencie <li>
        found_first_parent = main_category.find('a')
        # sprawdzamy, czy znaleziony link ma tekst równy wartości zmiennej kategoria
        if found_first_parent and found_first_parent.text.strip() == kategoria:
            parent_category = main_category  # Jeśli tak, to przypisujemy element li
            break
            #parent category to kawalek kodu html zawwierajacy calosc znalezionego <li></li> danej kategorii
    # warunek na przypadek gdy kategoria nie ma podkategori (parent_category=None)
    if parent_category:
        #znajdujemy wszystkie elementy <ul class="chidren"> </ul>
        children= parent_category.find('ul', class_='children')
        #znajdujemy <li> tylko bezpośrednie dzieci (pierwszy poziom podkategorii) dla children (recursive=False)
        all_subcategories=children.find_all('li', recursive=False)
        for subcategory in all_subcategories:
            found_subcategory = subcategory.find('a')
            name_subcategory=found_subcategory.text.strip()
            link_to_subcategory=found_subcategory['href']
            subcategories=getSubcategories(name_subcategory,link_to_subcategory)
            subcategories_dic[name_subcategory] ={
                'link': link_to_subcategory,
                'subcategories':subcategories
            }
    return subcategories_dic



def getCategories(soup):
    linkToCategories = soup.find("a", class_="elementor-item",string="Wszystkie produkty")
    urlCategories = linkToCategories["href"]
    pageCategories=urlopen(urlCategories)
    html_bytes_ctageories = pageCategories.read()
    html_categories = html_bytes_ctageories.decode("utf-8")
    soup=BeautifulSoup(html_categories, "html.parser")
    main_categories = soup.select("ul.product-categories > li.cat-item > a")
    # oddzielamy nazwy głównych kategorii
    main_category_names = []
    for category in main_categories:
        main_category_names.append((category.text.strip(),category['href']))
    #wypisane zostały kategorie podwójnie (implementacja obsługi na komputerach i urządzeniach mobilnych) dlatego pozbywamy się duplikatów
    unique_category_names = []
    categories_dic={}

    for category in main_category_names:
        if category not in unique_category_names:
            unique_category_names.append((category[0],category[1]))
    for category in unique_category_names:

        subcategories=getSubcategories(category[0],category[1])
        categories_dic[category[0]]={
            'link':category[1],
            'subcategories':subcategories
        }

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(categories_dic, json_file, ensure_ascii=False, indent=4)


url = "https://magiccafe.eu/"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

#getCategories(soup)

def getCategoriesNames(categoriesFile):
    with open(categoriesFile, 'r', encoding='utf-8') as f:
        return json.load(f)

def getProducts(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Nie udało się pobrać strony. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    # bierzemy wszystkie produkty
    try:
        products = soup.select(".jet-woo-products__item.jet-woo-builder-product")
        print(f"Znaleziono {len(products)} produktów na stronie: {url}")
        productLinks = []
        for product in products:
            productUrl = product.select_one(".jet-woo-item-overlay-link")['href']
            productLinks.append(productUrl)

        return productLinks

    except Exception as e:
        print(f"Nie udało się pobrać produktów z {url}: {e}")
        return []

def downloadProductImage(imageUrl, folder = 'images'):
    imageName = imageUrl.split("/")[-1]
    savePath = os.path.join(folder, imageName)

    response = requests.get(imageUrl, stream=True)
    if response.status_code == 200:
        with open(savePath, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return imageName
    return None

def getProductDetails(productUrl):
    response = requests.get(productUrl)
    if response.status_code != 200:
        print(f"Nie udało się pobrać strony produktu. Status code: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        # pobieramy wszystkie dane danego produktu
        name = soup.select_one(".product_title").text.strip()
        priceContainer = soup.find('span', class_='price')
        priceElement = priceContainer.find('span', class_='woocommerce-Price-amount')
        price = priceElement.text.strip()
        descriptionElement = soup.select_one("#tab-description")
        description = descriptionElement.text.strip() if descriptionElement else "" # jak nie bedzie opisu dla produktu to zostawiamy puste pole
        stock = soup.select_one(".stock").text.strip()
        productImageUrl = soup.select_one(".woocommerce-product-gallery__image img")['src']
        productImageName = downloadProductImage(productImageUrl)

        additionalInfo = {}
        attributesTable = soup.select_one(".woocommerce-product-attributes.shop_attributes")
        if attributesTable:
            rows = attributesTable.find_all("tr")
            for row in rows:
                label = row.find("th").text.strip()  # pobieramy nazwę atrybutu
                value = row.find("td").text.strip()  # pobieramy wartość atrybutu
                additionalInfo[label] = value

        # jeśli produkt nie posiada dodatkowych informacji to zostawiamy puste
        if not additionalInfo:
            additional_info = ""

        productDetails = {
            "name": name,
            "price": price,
            "description": description,
            "additional info": additionalInfo,
            "stock": stock,
            "image": productImageName,
            "url": productUrl
        }

        return productDetails

    except Exception as e:
        print(f"Nie udało się pobrać szczegółów produktu z {productUrl}: {e}")
        return {}


def processSubcategories(subcategories):
    productsData = {}

    for subcategoryName, subcategoryInfo in subcategories.items():
        #print(f"Pobieranie produktów z podkategorii: {subcategoryName} (Link: {subcategoryInfo['link']})")

        productLinks = getProducts(subcategoryInfo['link'])

        products = []
        for productUrl in productLinks:
            productDetails = getProductDetails(productUrl)
            if productDetails:
                products.append(productDetails)

        productsData[subcategoryName] = {
            "link": subcategoryInfo['link'],
            "products": products
        }

        if subcategoryInfo['subcategories']:
            productsData[subcategoryName]['subcategories'] = processSubcategories(subcategoryInfo['subcategories'])

    return productsData


def processCategories(categories):
    allCategoriesData = {}

    for categoryName, categoryInfo in categories.items():
        categoryData = {
            "link": categoryInfo['link'],
            "products": []  # narazie nie pobieramy dla kaltegorii tylko dla samych podkategorii
        }

        if categoryInfo['subcategories']:
            categoryData['subcategories'] = processSubcategories(categoryInfo['subcategories'])

        allCategoriesData[categoryName] = categoryData

    return allCategoriesData


def saveProductsToJson(productsData, outputFile):
    with open(outputFile, 'w', encoding='utf-8') as f:
        json.dump(productsData, f, ensure_ascii=False, indent=4)
    print(f"Produkty zapisane do pliku: {outputFile}")



categoriesFile = 'data.json'
productsFile = 'test.json'

categories = getCategoriesNames(categoriesFile)

#
products_data = processCategories(categories)
#
saveProductsToJson(products_data, productsFile)

