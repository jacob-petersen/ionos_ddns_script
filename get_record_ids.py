import requests
import json
from dotenv import load_dotenv
import os 

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_KEY_PUBLIC = os.getenv('API_KEY_PUBLIC')

"""
Gets a list of desired record types from the user.
"""
def getRecordTypes():

    def checkValidInput(inputList):

        validTypes = ['a', 'aaaa', 'cname', 'mx', 'ns', 'ptr', 'soa', 'srv', 'txt']

        for s in inputList:
            if s.lower() not in validTypes:
                return False
        
        return True
    
    print('Enter record types (A, AAAA, CNAME, MX, NS, PTR, SOA, SRV, TXT) (space-separated)')
    
    validInput = False
    
    while not validInput:
        recordTypes = input('>>> ')
        recordTypes = recordTypes.split(' ')
        recordTypes = [s.strip() for s in recordTypes]
        recordTypes = list(dict.fromkeys(recordTypes)) # removes duplicates

        if checkValidInput(recordTypes) == True:
            validInput = True
        else:
            print('Invalid input detected. Please enter from available record types.')

    return recordTypes


"""
Get the ID of the domain containing the subdomains that we are trying to identify
"""
def getDomainID():

    def checkValidInput(input, max):
        if input.isdigit() and (int(input) - 1) < max and (int(input) - 1) >= 0:
            return True
        else:
            return False

    url = 'https://api.hosting.ionos.com/dns/v1/zones'

    request_headers = {
        'X-API-Key': '{}.{}'.format(API_KEY_PUBLIC, API_KEY)
    }

    response = requests.get(url, headers=request_headers)
    responseArray = response.json()
    
    print('The following domains were returned:')
    for i in range(0, len(responseArray)):
        print('[{}] {} : {}'.format(i+1, responseArray[i]['name'], responseArray[i]['id']))

    print('Enter selection number (1-{})'.format(len(responseArray)))
    selectionNo = input('>>> ')
    
    validInput = False
    while not checkValidInput(selectionNo, len(responseArray)):
        print('Invalid input detected. Please enter a valid number (1-{})'.format(len(responseArray)))
        selectionNo = input('>>> ')

    selectionNo = int(selectionNo)

    return responseArray[selectionNo - 1]['id']

"""
Get all the domain records associated with domainID and of type(s) desired, and print in human-readable format
"""
def getDomainRecords(domainID, recordTypes):
    url = 'https://api.hosting.ionos.com/dns/v1/zones/' + domainID

    request_headers = {
        'X-API-Key': '{}.{}'.format(API_KEY_PUBLIC, API_KEY)
    }

    request_params = {
        'recordType': ','.join(recordTypes)
    }

    response = requests.get(url, headers=request_headers, params=request_params)

    print('Received the following records:')
    for i in range (0, len(response.json()['records'])):
        print('[{}] {} : {}'.format(i + 1, response.json()['records'][i]['name'], response.json()['records'][i]['id']))

def main():

    domainID = getDomainID()
    recordTypes = getRecordTypes()
    getDomainRecords(domainID, recordTypes)

    

main()