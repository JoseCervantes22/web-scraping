import requests
from bs4 import BeautifulSoup
import json

# URL de la página principal
url = "https://calhr.benefitsprograms.info/"

# Realiza una solicitud GET a la página principal
response = requests.get(url)

# Comprueba si la solicitud fue exitosa
if response.status_code == 200:
    # Analiza el HTML de la página principal
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encuentra el menú de navegación principal
    main_menu = soup.find('ul', id='top-menu')

    # Encuentra todos los elementos de menú (li) con enlaces (a)
    menu_items = main_menu.find_all('li', class_='menu-item')

    # Itera a través de los elementos de menú para extraer títulos y enlaces
    for menu_item in menu_items:
        menu_link = menu_item.find('a')
        menu_title = menu_link.text
        menu_url = menu_link['href']
        
        # Realiza una solicitud GET a la subpágina
        subpage_response = requests.get(menu_url)
        
        # Comprueba si la solicitud a la subpágina fue exitosa
        if subpage_response.status_code == 200:
            # Analiza el HTML de la subpágina
            subpage_soup = BeautifulSoup(subpage_response.text, 'html.parser')
            
            # Encuentra el contenido que deseas extraer (por ejemplo, un div con una clase específica)
            content_div = subpage_soup.find('div', class_='et_pb_section et_pb_section_1 et_section_regular')
            
            if content_div:
                print("Título de la página:", menu_title)
                print("Contenido de la página:")
                print(content_div.text)
                print("Link:", menu_url)
            else:
                print(f"No se encontró contenido en la subpágina: {menu_url}")
        
else:
    print("La solicitud a la página principal no fue exitosa. Código de estado:", response.status_code)
