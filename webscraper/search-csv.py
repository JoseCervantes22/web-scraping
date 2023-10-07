import pandas as pd # Install pandas: pip install pandas
import json # No need to install json; it's part of Python's standard library
import requests # Install requests: pip install requests

search_service_name = 'YOUR_SEARCH_SERVICE_NAME.search.windows.net'
index_name = 'YOUR_INDEX_NAME'
api_version = 'YOUR_API_VERSION'  # The version of the API you are using

api_key = 'YOUR_API_KEY' # The API you are using
headers = {
    'Content-Type': 'application/json',
    'api-key': api_key
}

url = f'https://{search_service_name}/indexes/{index_name}/docs/index?api-version={api_version}'

# Replace 'YOUR_ACCESS_TOKEN' with your personal GitHub access token
token = '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'

# CSV file URL
url_csv = f"https://raw.githubusercontent.com/JoseCervantes22/Q-A/main/BenieTraining.csv?token={token}"

# Read the CSV file
data = pd.read_csv(url_csv)

# Initialize a counter for the ID
id_counter = 102

# Iterate through the rows of the DataFrame
for index, row in data.iterrows():
    print(f"Row {index + 1}:")
    
    # Iterate through the rows of the DataFrame
    department = row['Department']
    question = row['Questions']
    answer = row['Answers']
    csv_url = row['url']
    combined_text = f"Question: {question}\nAnswer: {answer}"
    id_counter += 1
    
    
    data_to_send = {
        "@search.score": 1,
        "value": [
            {
                "id": str(id_counter),
                "title": department,  
                "content": combined_text,
                "url": csv_url
            }
        ]
    }
    # Print the values in the desired format
    print(f"    Title: {department}")
    print(f"    Content: {question}")
    print(f"    Answers: {answer}")
    print("Url: ",csv_url)

    # Increment the counter for the next ID
    id_counter += 1

    # Convert data to JSON
    data_json = json.dumps(data_to_send)

    # Make the POST request
    response = requests.post(url, headers=headers, data=data_json)

    # Check if the request was successful
    if response.status_code == 201:
        print('Documento enviado con éxito al índice.')
    else:
        print(f'Código de estado: {response.status_code}')
        print(response.text)
