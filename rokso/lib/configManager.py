import json, sys


class ConfigManager():

    def __init__(self):
        print("....")
        self.config = {}
        pass

    def __init__(self, filename) :
        """ Read config.json from project root if not found then throw an error """
        print("....", filename )
        self.config = {}
        try:
            with open('filename', 'r') as f:
                self.config = json.load(f)
        except:
            print("there is no config file in project root. Please run rokso init command.")


    def create_config(self, filename):
        # create a new config file in project root
        config_json = {}
        with open(filename, 'w') as json_file:
            json.dump(config_json, json_file, indent = 4, sort_keys=True)


    def get_config(self):
        return self.config