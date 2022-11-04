import json
from urllib.request import urlopen


def callApi(param: str) -> str:

    # import json

    # store the URL in url as
    # parameter for urlopen

    url = "http://45.63.39.115:8080"+param

    # store the response of URL

    response = urlopen(url)

    # storing the JSON response
    # from url in data

    data_json = json.loads(response.read())

    return str(data_json)


def get_response(message: str) -> str:
    p_message = message

    if 'getGetAllItems' in p_message and p_message.split(" ")[0] == 'getGetAllItems':
        print(p_message)
        if p_message.split(" ")[1] != "":
            return callApi('/getAllAtLocation?address=' + p_message.split(" ")[1])
        return 'Please enter location too'

    if p_message.lower() == '!help':
        return '`1. getGetAllItems <location>`'

    return 'I didn\'t understand what you wrote. Try typing "!help".'
