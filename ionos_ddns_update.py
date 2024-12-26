import requests
import json
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Import API private and public key from .env file
API_KEY = os.getenv('API_KEY')
API_KEY_PUBLIC = os.getenv('API_KEY_PUBLIC')
ZONE_ID = os.getenv('ZONE_ID')
DOMAIN_ID = os.getenv('DOMAIN_ID')

# Ionos DNS zones API base URL
url = 'https://api.hosting.ionos.com/dns/v1/zones/' + ZONE_ID + '/records/' + DOMAIN_ID

# Get the server's IP. Simple API call to ipify.org
ip = requests.get('https://api.ipify.org?format=json').json()['ip']
print('Public IP address: {}'.format(ip))

request_headers = {
    'X-API-Key': '{}.{}'.format(API_KEY_PUBLIC, API_KEY)
}

request_parameters = {
    'zoneId': ZONE_ID,
    'recordID': DOMAIN_ID
}

request_body = {
    'content': ip,
    'disabled': False,
    'ttl': 3600,
    'prio': 0
}

response = requests.put(url, headers=request_headers, params=request_parameters, json=request_body)
print('Code: {}'.format(response.status_code))
print(json.dumps(response.json(), indent=2))
