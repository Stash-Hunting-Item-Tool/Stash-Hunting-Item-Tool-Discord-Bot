import json
from urllib.request import urlopen
from table2ascii import table2ascii as t2a, PresetStyle

PAGE_LIMIT = 15


def convert_list_to_table(data_json: json, start=0) -> str:

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
                "z"],
        body=body,
        first_col_heading=True
    )

    return f"```\nItems from {start} to {start+PAGE_LIMIT} out of total {len(data_json)} for server <{data_json[0]['location']['locAddress']}>\n\n{output}\n```"


def convert_single_to_table(data_json: json) -> str:

    body = []

    body.append([
                0,
                data_json["id"],
                data_json["name"],
                data_json["qty"],
                data_json["location"]["locX"],
                data_json["location"]["locY"]])
    output = t2a(
        header=["row",
                "id",
                "name",
                "qty",
                "x",
                "z"],
        body=body,
        first_col_heading=True
    )

    return f"```\n{output}\n\nserver: {data_json['location']['locAddress']}\ncomment: {data_json['comment']}```"


def print_locations_table(data_json: json, start=0) -> str:

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
                        obj["locAddress"],
                        obj["locX"],
                        obj["locY"]])
    output = t2a(
        header=["row",
                "server",
                "x",
                "z"],
        body=body,
        first_col_heading=True
    )

    return f"```\nStashes from {start} to {start+PAGE_LIMIT} out of total {len(data_json)}\n\n{output}\n```"


def call_api(param: str) -> json:
    url = "http://45.63.39.115:8080"+param

    response = urlopen(url)

    return json.loads(response.read())


def convert_to_table(data_json: json, param: str, start=0) -> str:
    if "getAllLocations" in param:
        return print_locations_table(data_json, start=start)

    if "getFromId" in param:
        return convert_single_to_table(data_json)
    return convert_list_to_table(data_json, start=start)


def call_api_table_format(param: str, start=0) -> str:
    data_json = call_api(param)
    return convert_to_table(data_json, param, start=start)


def get_start_value(message: str) -> int:
    start_value = 0
    if len(message.split("start=")) == 2:
        start_value = int(message.split("start=")[1].split(" ")[0])
    return start_value


def get_response(message: str) -> str:
    p_message = message

    if 'getGetAllItems' in p_message and p_message.split(" ")[0] == 'getGetAllItems':
        print(p_message)
        address = p_message.split(" ")[1]
        if address != "":
            api_call = '/getAllAtLocation?address=' + address
            start_value = get_start_value(p_message)

            if len(p_message.split("name=")) == 2:
                name = p_message.split("name=")[1].split(" ")[0]
                return call_api_table_format(f"/getAllAtLocationWithName?address={address}&name={name}", start=start_value)

            return call_api_table_format(api_call, start=start_value)

        return 'Please enter location too'

    if 'getItem' in p_message:
        id = p_message.split(" ")[1]
        api_call = '/getFromId?id=' + id.strip()
        return call_api_table_format(api_call)

    if 'getAllStashes' in p_message:
        api_call = '/getAllLocations'
        if len(p_message.split("address=")) > 1:
            address = p_message.split("address=")[1].split(" ")[0]
            if address and address != "":
                data_jsons = call_api(api_call)
                data_jsons_cleaned = []
                for obj in data_jsons:
                    if obj["locAddress"] == address:
                        data_jsons_cleaned.append(obj)
                # return convert_to_table(data_jsons_cleaned, api_call,
                #                         start=get_start_value(p_message))

                return print_locations_table(data_jsons_cleaned, start=get_start_value(p_message))
        return call_api_table_format(api_call, start=get_start_value(p_message))

    if p_message.lower() == '!help':
        return '`1. getGetAllItems <location> start=<start optional>`'

    return 'I didn\'t understand what you wrote. Try typing "!help".'
