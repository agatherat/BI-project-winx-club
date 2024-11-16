from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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


def getCategoriesNames(categoriesFile):
    with open(categoriesFile, 'r', encoding='utf-8') as f:
        return json.load(f)


def getProducts(url):
    productLinks = set()  # na stronie istnieje bug (1 strona posiada 24 produkty, 2 posiada 12 produktów które znajdywały się na 1 stronie), więc pozbywamy się duplikatów

    driver = webdriver.Chrome()
    driver.get(url)

    while True:
        time.sleep(3)

        # czekamy, aż wszystkie produkty będą widoczne
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".jet-woo-products__item.jet-woo-builder-product"))
            )
        except Exception as e:
            print(f"Nie udało się załadować produktów: {e}")
            break

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup.select(".jet-woo-products__item.jet-woo-builder-product")

        # dla każdego produktu pobieramy jego url
        for product in products:
            productUrl = product.select_one(".jet-woo-item-overlay-link")['href']
            productLinks.add(productUrl)

        try:
            # sprawdzamy, czy przycisk 'Nast' jest dostepny i klikamy go
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".jet-filters-pagination__item.prev-next.next"))
            )

            if next_button:
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)
            else:
                break  # jeśli przycisk nie jest dostępny, oznacza to że nie ma następnej strony (lub cos nie zadziałało) więc przerywamy działanie funkcji

        except Exception as e:
            print(f"Brak kolejnych stron lub przycisk 'Nast' niedostępny: {e}")
            break  # nie udało się kliknąć przycisku, koniec wykonywania pętli

    driver.quit()
    return list(productLinks)


def downloadProductImage(imageUrl, folder = 'images'):
    # jeśli folder nie istnieje to najpierw go tworzymy
    if not os.path.exists(folder):
        os.makedirs(folder)

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

        summaryInner = soup.find('div', class_='summary-inner')
        priceContainer = summaryInner.find('p', class_='price')
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
            additionalInfo = ""

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


def processCategoryOrSubcategory(info):
    """Pobiera produkty i podkategorie dla danej kategorii lub podkategorii."""

    categoryData = {
        "link": info['link'],
        "products": []
    }

    # pobieramy produkty dla danej kategorii
    productLinks = getProducts(info['link'])
    products = []
    for productUrl in productLinks:
        productDetails = getProductDetails(productUrl)
        if productDetails:
            products.append(productDetails)

    categoryData['products'] = products

    # bedziemy przetwarzac podkategorie, jesli takowe istnieja
    if info['subcategories']:
        subcategoriesData = {}
        for subcategoryName, subcategoryInfo in info['subcategories'].items():
            subcategoriesData[subcategoryName] = processCategoryOrSubcategory(subcategoryInfo)

        categoryData['subcategories'] = subcategoriesData

    return categoryData


def processCategories(categories):
    allCategoriesData = {}

    for categoryName, categoryInfo in categories.items():
        allCategoriesData[categoryName] = processCategoryOrSubcategory(categoryInfo)

    return allCategoriesData


def saveProductsToJson(productsData, outputFile):
    with open(outputFile, 'w', encoding='utf-8') as f:
        json.dump(productsData, f, ensure_ascii=False, indent=4)
    print(f"Produkty zapisane do pliku: {outputFile}")


url = "https://magiccafe.eu/"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

getCategories(soup)  # pobieramy nazwy kategorii i ich podkategorii
categoriesFile = 'data.json'  # w tym pliku przechowujemy nazwy kategorii i podkategorii
productsFile = 'products.json'  # w tym pliku przechowujemy dane o produktach
categories = getCategoriesNames(categoriesFile)  # z pliku wyciągamy nazwy kategorii
products_data = processCategories(categories)  # pobieramy dane produktów
saveProductsToJson(products_data, productsFile)   # zapisujemy pobrane dane do pliku
