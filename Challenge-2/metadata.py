import requests
import json

metadata_url = 'http://169.254.169.254/latest/'


def expand_tree(url, arr):
    output = {}
    for term in arr:
        new_url = url + term
        r = requests.get(new_url)
        text = r.text
        if term[-1] == "/":
            list_of_values = r.text.splitlines()
            output[term[:-1]] = expand_tree(new_url, list_of_values)
        elif check_if_json(text):
            output[term] = json.loads(text)
        else:
            output[term] = text
    return output


def get_metadata():
    initial = ["meta-data/"]
    result = expand_tree(metadata_url, initial)
    return result


def get_metadata_json():
    metadata = get_metadata()
    metadata_json = json.dumps(metadata, indent=4, sort_keys=True)
    return metadata_json


def check_if_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


if _name_ == '_main_':
    print(get_metadata_json())
