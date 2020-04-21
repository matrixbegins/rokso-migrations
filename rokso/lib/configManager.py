import json, sys, os


class ConfigManager():

    initial_dirs = ["migration"]

    def create_inital_dirs(self, working_dir):
        print("[#] Generating required dir(s) if not exist")

        for dir in self.initial_dirs:
            dirname = working_dir + "/" + dir
            if not os.path.isdir(dirname):
                try:  
                    os.mkdir(dirname)  
                except Exception as e:  
                    raise e 

    def __init__(self, json_dict, cwd):        
        # create a new config file in project root

        CONFIG_FILE = cwd + "/" + "config.json"

        print("[*] Checking state of config file in CWD")
        if os.path.exists(CONFIG_FILE):
            print("[#] Config file already exists")
        else:

            json_data = { "database": json_dict }
            json_object = json.dumps(json_data, indent = 4, sort_keys=True) + "\n"

            with open(CONFIG_FILE, "w") as config_file:
                config_file.write(json_object)
                print("[*] Config file has been created")

            self.create_inital_dirs(cwd)


    def get_config(self, cwd):
        CONFIG_FILE = cwd + "/" + "config.json"
        self.create_inital_dirs(cwd)
        try:
            with open(CONFIG_FILE, 'r') as f:
                 config = f.read()
        except Exception as e:
            raise e

        return config