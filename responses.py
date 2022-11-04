import json
from urllib.request import urlopen
from table2ascii import table2ascii as t2a, PresetStyle

PAGE_LIMIT = 15


def convert_to_table(data_json: json, start=0) -> str:

    body = []

    total_count = 0
    count = 0
    for obj in data_json:

        total_count += 1

        if total_count > start:

            if count > PAGE_LIMIT:
                break
            count += 1

            body.append([
                        total_count-1,
                        obj["id"],
                        obj["name"],
                        obj["qty"],
                        obj["location"]["locX"],
                        obj["location"]["locY"]])
    output = t2a(
        header=["row",
                "id",
                "name",
                "qty",
                "x",
                "y"],
        body=body,
        first_col_heading=True
    )

    return f"```\nItems from {start} to {start+PAGE_LIMIT} for server <{data_json[0]['location']['locAddress']}>\n\n{output}\n```"


def callApi(param: str, start=0) -> str:

    # import json

    # store the URL in url as
    # parameter for urlopen

    url = "http://45.63.39.115:8080"+param

    # store the response of URL

    response = urlopen(url)

    # storing the JSON response
    # from url in data

    data_json = json.loads(response.read())

    return convert_to_table(data_json, start=start)


def get_response(message: str) -> str:
    p_message = message

    if 'getGetAllItems' in p_message and p_message.split(" ")[0] == 'getGetAllItems':
        print(p_message)
        address = p_message.split(" ")[1]
        if address != "":
            api_call = '/getAllAtLocation?address=' + address
            start_value = 0
            if len(p_message.split("start=")) == 2:
                start_value = int(p_message.split("start=")[1].split(" ")[0])
            return callApi(api_call, start=start_value)
        return 'Please enter location too'

    if p_message.lower() == '!help':
        return '`1. getGetAllItems <location> start=<start optional>`'

    return 'I didn\'t understand what you wrote. Try typing "!help".'
