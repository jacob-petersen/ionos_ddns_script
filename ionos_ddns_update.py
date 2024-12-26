import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime

# Simple logging function. I don't want to use the logging library
def log_message(message, include_time=False, file_path='ddns.log'):
    with open(file_path, 'a') as file:
        if include_time:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write('{} {} =============================================\n'.format(timestamp, datetime.now().astimezone().tzinfo))
        
        file.write('{}\n'.format(message))

# Load variables from .env file
load_dotenv()

# Import API private and public key from .env file
API_KEY = os.getenv('API_KEY')
API_KEY_PUBLIC = os.getenv('API_KEY_PUBLIC')
ZONE_ID = os.getenv('ZONE_ID')
DOMAIN_ID = os.getenv('DOMAIN_ID')
LOGGING = os.getenv('LOGGING')

# Verify the presence of all environment variables
for v_name, v_val in {'API_KEY':API_KEY, 'API_KEY_PUBLIC':API_KEY_PUBLIC, 'ZONE_ID':ZONE_ID, 'DOMAIN_ID':DOMAIN_ID, 'LOGGING':LOGGING}.items():
    if not v_val: # checks for empty strings, None type, etc
        print('Missing environment variable {} ! Check your .env file.'.format(v_name))
        exit()

# Set LOGGING to True or False depending on value, print error if invalid
if LOGGING.lower() in ['true', '1']:
    LOGGING = True
elif LOGGING.lower() in ['false', '0']:
    LOGGING = False
else:
    print('Invalid value of LOGGING: \"{}\". Check your .env file!'.format(LOGGING))
    exit()

# Ionos DNS zones API base URL
url = 'https://api.hosting.ionos.com/dns/v1/zones/' + ZONE_ID + '/records/' + DOMAIN_ID

# Get the server's IP. Simple API call to ipify.org
ip = requests.get('https://api.ipify.org?format=json').json()['ip']

# Ionos API request headers, parameters, and body
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

print('Public IP address: {}'.format(ip))

if LOGGING:
    log_message('Starting DNS Update', include_time=True)
    log_message('Public IP address {}'.format(ip))

response = requests.put(url, headers=request_headers, params=request_parameters, json=request_body)

print('Response from server: {}'.format(response.status_code))

if response.status_code == 200:
    print('Updated record {} to {}'.format(response.json()['name'], response.json()['content']))
    if LOGGING:
        log_message('Updated record {} to {}'.format(response.json()['name'], response.json()['content']))
else:
    print('Message: {}'.format(response.json()['message']))
    if LOGGING:
        log_message('Message: {}'.format(response.json()['message']))