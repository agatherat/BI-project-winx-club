from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


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

getCategories(soup)