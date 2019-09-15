import json


def spec_read():
    with open('spec.json', 'r') as f:
        return json.load(f)


spec = spec_read()
