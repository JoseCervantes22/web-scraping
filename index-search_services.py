import requests
from bs4 import BeautifulSoup
import json

search_service_name = 'securygpt.search.windows.net'
index_name = 'index-website'
api_version = '2023-07-01-Preview'

# URL del servicio de búsqueda
search_url = f'https://{search_service_name}/indexes/{index_name}/docs/index?api-version={api_version}'

# Definir el encabezado de autorización (necesitarás un token de autenticación)
api_key = 'ASkaLb4Ob0QcGCPDUlcEAv9FV7565ihYjK34SWYFzNAzSeD5XUar'
headers = {
    'Content-Type': 'application/json',
    'api-key': api_key
}

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
                
                
                data_to_send = {
                    "@search.score": 1,
                    "value": [
                    {
                        "id": "1",
                        "website": menu_title,  
                        "content": content_div.text,
                        "link": menu_url
                    }
                    ]
                }

                data_json = json.dumps(data_to_send)

                # Realizar la solicitud POST al servicio de búsqueda
                response = requests.post(search_url, headers=headers, data=data_json)
                if response.status_code == 201:
                    print('Documento enviado con éxito al índice.')
                else:
                    print(f'Error al enviar el documento. Código de estado: {response.status_code}')
                    print(response.text)

            else:
                print(f"No se encontró contenido en la subpágina: {menu_url}")
        
else:
    print("La solicitud a la página principal no fue exitosa. Código de estado:", response.status_code)
