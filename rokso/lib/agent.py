import sys, click
from .configManager import ConfigManager
from .dbManager import DBManager
from .migrationManager import MigrationManager
import json
import os

json_dict = {}
initial_dirs = ["migration"]

def custom_exit(CODE, message = " "):

    print("[#] Oooo... snap     \_(-_-)_/ ")
    print(message)
    exit(CODE)

def init_setup(dbhost, dbname, dbusername, dbpassword, projectpath):
    """
        This function will check/create the config.json in project root.
        then it'll check/create the revision table in database
    """
    CONFIG_FILE = projectpath + "/" + "config.json"

    print("[*] Checking state of any config file inside project dir")
    if os.path.exists(CONFIG_FILE):
        custom_exit(1, "Config file already exist, exiting")

    json_dict["host"] = dbhost
    json_dict["database"] = dbname
    json_dict["user"] = dbusername
    json_dict["password"] = dbpassword
 
    json_data = { "database": json_dict }
    json_object = json.dumps(json_data, indent = 4, sort_keys=True) + "\n"
    
    if not os.path.isdir(projectpath):
       try:  
            os.mkdir(projectpath)  
       except Exception as e:  
            custom_exit(1, e)

    with open(CONFIG_FILE, "w") as config_file:
        config_file.write(json_object)
        print("[*] Config file has been created")

    print("[*] Creating required dirs")

    for dir in initial_dirs:
       directory_path = projectpath + "/" + dir
       try:  
            os.mkdir(directory_path)  
       except Exception as e:  
            custom_exit(1, e)        



def db_status():
    """
    Checks all the migrations processed so far from database
    then checks all pending migrations.
    """
    pass


def create_db_migration(tablename, filename):
    pass


def rollback_db_migration(version):
    pass


def reverse_enginner_db():
    """
        1. finds all the tabels in database
        2. extract the table definition for each table from DB
        3. create the migration files under "migrations" dir located in project root.
    """
    pass


