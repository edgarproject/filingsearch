import json
import os


class ReadJson:

    def __init__(self):
        self.path = os.getcwd().replace("spiders","configurations\setting.json")
        with open(self.path, 'r') as data:
            self.data = json.loads(data.read())

    def get_json_key(self, key):
        return self.data[key]

