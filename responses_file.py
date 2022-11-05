import requests
import utils
import config


def split_packet_content(line: str) -> list:
    words = line.split(" ")
    slot = ""
    stack = ""
    windowId = ""
    next_slot = False
    next_stack = False
    next_windowId = False
    for word in words:
        if next_slot:
            slot = word
            next_slot = False
        if next_stack and word != "windowId:":
            stack = f"{stack} {word}"
        if next_windowId:
            windowId = word
            next_windowId = False

        if word == "slot:":
            next_slot = True
        if word == "stack:":
            next_stack = True
        if word == "windowId:":
            next_windowId = True
            next_stack = False
    return [int(slot), stack.strip(), int(windowId)]


def add_file_to_db(message, p_message: str, url: str) -> str:
    file_request = requests.get(message.attachments[0].url)
    file = str(file_request.content).split("\\n")

    items = {}
    for line in file:
        if "SPacketSetSlot" in line:
            line_content = split_packet_content(line.split(",")[4])
            if(line_content[0] < 55 and line_content[0] >= 0):
                if not items.__contains__(line_content[1]):
                    items[line_content[1]] = 1
                items[line_content[1]] = items[line_content[1]]+1
    print("items")
    print(items)

    x = utils.get_value_by_name(p_message, "x")
    z = utils.get_value_by_name(p_message, "z")
    address = utils.get_value_by_name(p_message, "address")
    print(f"other details: \n x: {x}, y: {z},address: {address} ")
    if(x == "" or z == "" or address == ""):
        return "please use `addFile x=<x> z=<z> address=<server adddress> <drag your packet file>`"

    url = config.URL+"/addItem"
    for item in items:
        data = {"name": f"{item}",
                "qty": items[item],
                "comment": "done by discord bot",
                "location": {
                    "locX": x,
                    "locY": z,
                    "locAddress": address
                }
                }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)
        res = response.json()
        print(res)

    return "ok"
