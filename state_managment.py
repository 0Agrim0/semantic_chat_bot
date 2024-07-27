import json


def get_state():
    f = open('state.json')
    data = json.load(f)
    return data


def set_state(phone, main_flow, next_function_call):
    dictionary = {
        phone: {
            "main_flow": main_flow,
            "next_function_call": next_function_call
        }
    }
    json_object = json.dumps(dictionary, indent=4)

    with open("state.json", "w") as outfile:
        outfile.write(json_object)


def add_state(phone, main_flow, next_function_call):
    data = get_state()
    data[phone] = {
        "main_flow": main_flow,
        "next_function_call": next_function_call
    }
    json_object = json.dumps(data, indent=4)
    with open("state.json", "w") as outfile:
        outfile.write(json_object)
