import json, sys, os
import importlib
import importlib.util
from datetime import datetime

migration_file_template = """apply_sql = \"""
%s
\"""

rollback_sql = "%s"

migrations = {
    "apply": apply_sql,
    "rollback": rollback_sql
}
"""

empty_migration_template = migration_file_template % ('WRITE your DDL/DML query here', 'WRITE your ROLLBACK query here.')


class MigrationManager:
    def __init__(self, path):
        self.migration_path = path
        sys.path.append(self.migration_path)
        pass


    def module_from_file(self, module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


    def import_migration_files(self):
        for main_dir, subdirs, files in os.walk(self.migration_path):
            print('\n\nprocessing directory: ', main_dir)
            print('subdirectory: ', subdirs)
            if "__pycache__" in main_dir:
                continue
            for f in files:
                print("processing file:: ", f)
                modulename = f.strip('.py')
                module = self.module_from_file(os.path.basename(main_dir) + '_' + modulename , main_dir + os.path.sep + f)

                print(module.migrations)


    def import_single_migration(self, table_name:str, file_name:str):
        full_path = self.migration_path + os.path.sep + table_name + os.path.sep + file_name
        if os.path.exists(full_path):
            modulename = file_name.strip('.py')
            module = self.module_from_file(table_name + '_' + modulename , full_path)
            print(module.migrations)
            return module.migrations
        else:
            return None


    def create_migration_file(self, table_name, file_name):
        new_file_name = self.get_new_file_name(file_name)
        self.create_dir_write_file(table_name, new_file_name, empty_migration_template)

        print("[*] migration file {} has been generated".format(new_file_name) )


    def create_dir_write_file(self, table_name, file_name, content):
        dir_path = self.migration_path + os.path.sep + table_name
        if not os.path.exists(dir_path):
            if not os.path.isdir(dir_path):
                try:
                    os.mkdir(dir_path)
                except Exception as e:
                    raise e

        mg_file = open(dir_path + os.path.sep + file_name, "w+")
        mg_file.write(content)
        mg_file.close()


    def get_new_file_name(self, file_name):
        now = datetime.now()
        time_part = now.strftime("%Y_%m_%d__%H_%M_%S")
        name_temp = "{}_{}.py"
        return name_temp.format(time_part, file_name)


    def get_all_migration_files(self):
        list1 = []
        for main_dir, subdirs, files in os.walk(self.migration_path):
            print('\n\nprocessing directory: ', main_dir)
            if "__pycache__" in main_dir:
                continue
            for f in files:
                print('checking::', main_dir + os.path.sep + f )

                list1.append(main_dir + os.path.sep + f)

        return list1


    def create_migration_file_with_sql(self, table_name:str, create_sql:str):
        file_name = self.get_new_file_name('create_table_' + table_name )

        drop_sql = "DROP TABLE IF EXISTS {} ;".format(table_name)
        content = migration_file_template % (create_sql, drop_sql)
        self.create_dir_write_file(table_name, file_name, content)

        print("file {}{}{} has been created.".format(table_name, os.path.sep, file_name))
        return table_name + os.path.sep + file_name

