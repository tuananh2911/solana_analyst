import json


def parse_to_json(self, data):
    return json.dumps(data, indent=4)


def save_data_to_file(self, data, filename):
    with open(filename, 'w') as f:
        f.write(data)