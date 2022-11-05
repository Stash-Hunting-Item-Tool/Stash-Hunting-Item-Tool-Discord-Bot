
import json
from urllib.request import urlopen
import config


def get_value_by_name(message: str, value_name: str) -> str:
    value = ""
    if len(message.split(f"{value_name}=")) == 2:
        value = message.split(f"{value_name}=")[1].split(" ")[0]
    return value


def call_api(param: str) -> json:
    url = config.URL+param

    response = urlopen(url)

    return json.loads(response.read())
