import requests  # Install requests: pip install requests

from bs4 import BeautifulSoup  # Install beautifulsoup4: pip install beautifulsoup4

import json  # No need to install json; it's part of Python's standard library

search_service_name = 'YOUR_SERVICE_NAME.search.windows.net'
index_name = 'YOUR_INDEX'
api_version = '2023-07-01-Preview'  # The version of the API you are using

api_key = 'YOUR_API_SEARCH' # The API you are using
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

login_url=('https://calhr.benefitsprograms.info/wp-login.php?action=postpass')

payload={
    'post_password':'2021StateHRP'
}
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
                        "Title": menu_top_title,  
                        "Content": content_div.text,
                        "URL": menu_top_url
                    }
                ]
            }
            # Convert data to JSON
            data_json = json.dumps(data_to_send)
            response = requests.post(cognitive_url, headers=headers, data=data_json)
            # Check if the request was successful
            if response.status_code == 200:
                print('Document successfully sent to index.')
            else:
                print(f'Error sending document. Status code: {response.status_code}')
           
            content_links = [] 

            social_media = ['facebook.com', 'twitter.com', 'instagram.com']
            if content_div:
                links_in_content = content_div.find_all('a')
                
                
                for link in links_in_content:
                    href = link.get('href')

                
                    if href and href not in content_links and not any(rs in href for rs in social_media) and href.startswith("https://calhr.benefitsprograms.info/"):
                        content_links.append(href)
                        content_div_content_links = subpage_soup.find('div', class_='et_pb_section et_pb_section_1 et_section_regular')
                    
                        if content_div_content_links:
                            print("Title")
                            print('Content:')
                            print(content_div_content_links.text)
                            print("Link: ",href)
                            print('id',str(id_counter))
                            data_to_send = {
                                "@search.score": 1,
                                "value": [
                                    {
                                        "id": str(id_counter),
                                        "Title": "",  
                                        "Content": content_div.text,
                                        "URL": href
                                    }
                                ]
                            }
                            # Convert data to JSON
                            data_json = json.dumps(data_to_send)
                            response = requests.post(cognitive_url, headers=headers, data=data_json)
                            # Check if the request was successful
                            if response.status_code == 200:
                                print('Document successfully sent to index.')
                            else:
                                print(f'Error sending document. Status code: {response.status_code}')
              
                        else:
                            print('Not content')
                    elif href:
                        print('content_repeat')
                        
             

            else:
                print(f"Content from login:{menu_top_url}")
            
                with requests.session() as s:
                    s.post(login_url, data=payload)
                    r=s.get(menu_top_url)
                    menu_top_link = menu_top_item.find('a')
                    menu_top_title = menu_top_link.text
                    soup=BeautifulSoup(r.content,'html.parser')
                    content_div = soup.find('div', class_='et_pb_section et_pb_section_1 et_section_regular')
                    if content_div:
                        print("Page title:", menu_top_title)
                        print("Content:")
                        print(content_div.text)
                        print("link",menu_top_url)
                        print("id",str(id_counter))
                        
                        data_to_send = {
                            "@search.score": 1,
                            "value": [
                                {
                                    "id": str(id_counter),
                                    "Title": menu_top_title,  
                                    "Content": content_div.text,
                                    "URL": menu_top_url
                                }
                            ]
                        }
                        # Convert data to JSON
                        data_json = json.dumps(data_to_send)
                        response = requests.post(cognitive_url, headers=headers, data=data_json)
                        # Check if the request was successful
                        if response.status_code == 200:
                            print('Document successfully sent to index.')
                        else:
                            print(f'Error sending document. Status code: {response.status_code}')
                        
                    else:
                        content_div_2 = soup.find('div', class_='et_pb_section et_pb_section_2 et_section_regular')
                        if content_div_2:
                            print("Page title:", menu_top_title)
                            print("Content")
                            print(content_div_2.text)
                            print("link ",menu_top_url)
                            print("id",str(id_counter))
                            
                            data_to_send = {
                                "@search.score": 1,
                                "value": [
                                    {
                                        "id": str(id_counter),
                                        "Title": menu_top_title,  
                                        "Content": content_div_2.text,
                                        "URL": menu_top_url
                                    }
                                ]
                            }
                            # Convert data to JSON
                            data_json = json.dumps(data_to_send)
                            response = requests.post(cognitive_url, headers=headers, data=data_json)
                            # Check if the request was successful
                            if response.status_code == 200:
                                print('Document successfully sent to index.')
                            else:
                                print(f'Error sending document. Status code: {response.status_code}')
                                
                        else:
                            print("No content")
                           
else:
    print("The request to the home page was not successful. Status code:", response.status_code)
