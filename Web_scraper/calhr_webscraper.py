import requests  # Install requests: pip install requests

from bs4 import BeautifulSoup  # Install beautifulsoup4: pip install beautifulsoup4

import json  # No need to install json; it's part of Python's standard library

search_service_name = 'YOUR_SEARCH_SERVICES.search.windows.net'
index_name = 'YOUR_INDEX'
api_version = 'YOUR_API_VERSION'  # The version of the API you are using


api_key = 'INSERT_YOUR_KEY' # The API you are using
headers = {
    'Content-Type': 'application/json',
    'api-key': api_key
}

# Construct the URL for a search request
cognitive_url = f'https://{search_service_name}/indexes/{index_name}/docs/index?api-version={api_version}'

# Home page URL CalHR benefits
url = "https://calhr.benefitsprograms.info/"

# Make a GET request to the main page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML of the main page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main navigation menu (menu-top)
    main_menu_top = soup.find('ul', id='top-menu')
    
    # Find all menu items (li) with links (a) in the menu-top
    menu_top_items = main_menu_top.find_all('li', class_='menu-item')

    id_counter=0
    
    # Iterate through top-menu items to extract titles and links
    print("Top-menu:")
    for menu_top_item in menu_top_items:
        menu_top_link = menu_top_item.find('a')
        menu_top_title = menu_top_link.text
        menu_top_url = menu_top_link['href']
        
        subpage_response = requests.get(menu_top_url)
        if subpage_response.status_code == 200:
            # Parse the HTML of the subpage
            subpage_soup = BeautifulSoup(subpage_response.text, 'html.parser')
            
            # Find the content you want to extract (for example, a div with a specific class)
            content_div = subpage_soup.find('div', class_='et_pb_section et_pb_section_1 et_section_regular')
            id_counter += 1
            if content_div:
                
                print("Page title:", menu_top_title)
                print("Content:")
                print(content_div.text)
                print("Link:", menu_top_url)
                print("id",str(id_counter))
                    
                
                data_to_send = {
                    "@search.score": 1,
                    "value": [
                        {
                            "id": str(id_counter),
                            "title": menu_top_title,  
                            "content": content_div.text,
                            "url": menu_top_url
                        }
                    ]
                }
                # Convert data to JSON
                data_json = json.dumps(data_to_send)
                response = requests.post(cognitive_url, headers=headers, data=data_json)
                # Check if the request was successful
                if response.status_code == 201:
                    print('Document successfully sent to index.')
                else:
                    print(f'Error sending document. Status code: {response.status_code}')
                
            else:
                print(f"No content found on subpage:{menu_top_url}")
        
else:
    print("The request to the home page was not successful. Status code:", response.status_code)
