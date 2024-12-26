import requests
import json
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Import API private and public key from .env file
API_KEY = os.getenv('API_KEY')
API_KEY_PUBLIC = os.getenv('API_KEY_PUBLIC')

# Ionos DNS zones API base URL
url = 'https://api.hosting.ionos.com/dns/v1/zones/' + '20a908db-14a9-11ec-81e7-0a5864444eb9'

request_headers = {
    'X-API-Key': '{}.{}'.format(API_KEY_PUBLIC, API_KEY)
}

request_parameters = {
    'zoneId': '20a908db-14a9-11ec-81e7-0a5864444eb9',
    'recordType': 'A'
}

request_body = {

}

response = requests.get(url, headers=request_headers, params=request_parameters)
print('Code: {}'.format(response.status_code))
print(json.dumps(response.json(), indent=2))
