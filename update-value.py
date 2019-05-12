import requests
import json
import sys

def updateValueOnEnvironment(apiKey, key, value):
    environmentData = requests.get('https://api.getpostman.com/environments', headers={"X-API-Key":apiKey})

    if environmentData.ok:
        environments = environmentData.json()['environments']
        for environment in environments: 
            environmentId = environment['id']
            environmentUrl = 'https://api.getpostman.com/environments/' + environmentId
            singleEnvData = requests.get(environmentUrl, headers={"X-API-Key":apiKey})

            if singleEnvData.ok:
                fullEnvironment = singleEnvData.json()['environment']

                values = fullEnvironment['values']

                index = -1
                i = 0

                action = 'updated'
                for item in values:
                    if item['key'] == key:
                        index = i
                        item['value'] = value
                        break
                    i = i + 1
                
                if (index == -1):
                    action = 'added'
                    values.append({
                        "key": key,
                        "value": value,
                        "enabled": True
                    })

                putResponse = requests.put(environmentUrl, data=json.dumps({'environment': fullEnvironment}), headers={"X-API-Key":apiKey})

                if(putResponse.ok):
                    print('Updating environment [' + fullEnvironment['name'] + ']: ' + action + ' key [' + key + '] with value [' + value + ']')

updateValueOnEnvironment(sys.argv[1], sys.argv[2], sys.argv[3])