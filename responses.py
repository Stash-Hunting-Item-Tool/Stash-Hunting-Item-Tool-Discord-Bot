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

    if "getFromId" in param or "changeItemQty" in param:
        return convert_single_to_table(data_json)
    return convert_list_to_table(data_json, start=start)


def call_api_table_format(param: str, start=0) -> str:
    data_json = call_api(param)
    return convert_to_table(data_json, param, start=start)


def get_start_value(message: str) -> int:
    raw_val = get_value_by_name(message=message, value_name="start")
    if raw_val.isdigit():
        return int(raw_val)
    return 0


def get_value_by_name(message: str, value_name: str) -> str:
    value = ""
    if len(message.split(f"{value_name}=")) == 2:
        value = message.split(f"{value_name}=")[1].split(" ")[0]
    return value


def get_response(message: str) -> str:
    p_message = message

    if 'getGetAllItems' in p_message and p_message.split(" ")[0] == 'getGetAllItems':
        address = get_value_by_name(p_message, "address")
        if address and address != "":
            api_call = '/getAllAtLocation?address=' + address
            start_value = get_start_value(p_message)

            name = get_value_by_name(p_message, "name")
            if name != "":
                return call_api_table_format(f"/getAllAtLocationWithName?address={address}&name={name}", start=start_value)

            return call_api_table_format(api_call, start=start_value)

        return 'Please enter location too'

    if 'getItem' in p_message:
        id = p_message.split(" ")[1]
        api_call = '/getFromId?id=' + id.strip()
        return call_api_table_format(api_call)

    if 'getAllStashes' in p_message:
        api_call = '/getAllLocations'
        address = get_value_by_name(p_message, "address")
        if address and address != "":
            data_jsons = call_api(api_call)
            data_jsons_cleaned = []
            for obj in data_jsons:
                if obj["locAddress"] == address:
                    data_jsons_cleaned.append(obj)

            return print_locations_table(data_jsons_cleaned, start=get_start_value(p_message))
        return call_api_table_format(api_call, start=get_start_value(p_message))

    if 'takeItem' in p_message:
        id = get_value_by_name(p_message, "id")
        if id and id != "":
            api_call = f"/changeItemQty?id={id}"
            qty = get_value_by_name(p_message, "qty")
            if qty and qty != "":
                api_call = f"{api_call}&qty={qty}"
            return call_api_table_format(api_call)
        return 'id is required'

    if p_message.lower() == '!help':
        help_string = '```\n1. getGetAllItems adress=<server adddress> start=<start optional>\n2. getItem <id>\n3. getAllStashes address=<server adddress optional> start=<start optional>\n4. takeItem id=<id> qty=<qty optional, default 1>```'
        return help_string

    return 'I didn\'t understand what you wrote. Try typing "!help".'
