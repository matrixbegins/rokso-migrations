import json, sys, os


class ConfigManager():

    initial_dirs = ["migration"]

    def __init__(self):
        self.config = {}


    def create_initial_dirs(self, working_dir:str):
        print("[#] Generating required dir(s) if not exist")

        for dir in self.initial_dirs:
            dirname = working_dir + os.path.sep + dir
            # print('creating:: ', dirname)
            if not os.path.isdir(dirname):
                try:
                    os.mkdir(dirname)
                except Exception as e:
                    raise e


    def init(self, json_dict:dict, cwd:str):
        # create a new config file in project root

        CONFIG_FILE = cwd + os.path.sep + "config.json"

        print("[*] Checking state of config file in CWD")
        if os.path.exists(CONFIG_FILE):
            raise FileExistsError("Config file already exists")
        else:
            json_data = { "database": json_dict }
            json_object = json.dumps(json_data, indent = 4, sort_keys=True) + "\n"

            with open(CONFIG_FILE, "w") as config_file:
                config_file.write(json_object)
                print("[*] Config file has been created")

            self.create_initial_dirs(cwd)


    def get_config(self, cwd:str):
        CONFIG_FILE = cwd + os.path.sep + "config.json"
        # print('reading config file::', CONFIG_FILE)
        if not bool(self.config):
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.loads(f.read())

        return self.config