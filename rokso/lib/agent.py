import sys, click
from .configManager import ConfigManager
from .dbManager import DBManager
from .migrationManager import MigrationManager
import json
import os


json_dict = {}
initial_dirs = ["migration"]

def custom_exit(CODE, ex, message = " "):

    print("[#] Oooo... snap     \_(-_-)_/ ")
    print(ex)
    print(message)
    exit(CODE)

def get_cwd():
    return os.getcwd()    

def init_setup(dbhost, dbname, dbusername, dbpassword, projectpath):
    """
        This function will check/create the config.json in project root.
        then it'll check/create the revision table in database
    """
    cwd = get_cwd()
    
    json_dict = { "host": dbhost, "databse": dbname, "user": dbusername, "password": dbpassword }
    
    try:
        CMobj = ConfigManager(json_dict, cwd)
    except Exception as e:
        custom_exit(1, e, "Issues while creating inital dirs")

    try:    
        config = CMobj.get_config(cwd)
    except Exception as e:
        custom_exit(1, "unable to read configuraion")    


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


