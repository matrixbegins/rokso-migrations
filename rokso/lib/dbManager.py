import mysql.connector
from mysql.connector import Error
from .connectionManager import ConnectionManager
from time import time

default_version_table_name = "rokso_db_version"

class DBManager:
    def __init__(self, config):
        self.revision_table = config.get("version_table_name", default_version_table_name)
        self.config = {k: config[k] for k in ('host', 'database', 'user', 'password')}


    def execute_query(self, sql):
        connection = ConnectionManager(self.config).get_connection()
        try:
            cursor = connection.cursor()
            print("\nExecuting>> ", sql )
            tic = time()
            cursor.execute(sql)
            connection.commit()
            toc = time()
            print("query completed successfully..")
            print(">> Time taken: {}secs ".format(round(toc - tic, 4)) )

        except Error as e:
            print("There was an error executing sql:: " + sql, "\n ❌", e)
            raise e
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()


    def select_query(self, sql):
        connection = ConnectionManager(self.config).get_connection()
        try:
            cursor = connection.cursor()
            print("\nExecuting>> ", sql )
            tic = time()
            cursor.execute(sql)
            toc = time()
            print(">> Time taken: {}secs ".format(round(toc - tic, 4)) )
            return cursor.column_names, cursor.fetchall()

        except Error as e:
            print("There was an error executing sql:: " + sql, "\n ❌", e)
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()


    def create_version_table(self):
        """ Creates database version table in the given database """

        sql = """
            CREATE TABLE IF NOT EXISTS {} (
                id INT auto_increment NOT NULL,
                filename varchar(255) NOT NULL,
                version varchar(100) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending' NOT NULL,
                scheduledAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                executedAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT id_PK PRIMARY KEY (id),
                CONSTRAINT filename_UNQ UNIQUE KEY (filename)
            ) ENGINE=InnoDB;
        """
        self.execute_query(sql.format(self.revision_table))
        pass


    def get_database_state(self):
        return self.select_query("SELECT * FROM {}".format(self.revision_table))


    def apply_migration(self, sql, filename, version ):

        try:
            self.execute_query(sql)
            self.insert_new_migration(filename, version, 'complete')
        except Error as e:
            self.insert_new_migration(filename, version, 'error')
            raise e


    def insert_new_migration(self, filename, version, status='pending' ):
        sql = """
                INSERT INTO {}
                (filename, version, status, scheduledAt, executedAt)
                VALUES('{}', '{}', '{}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON DUPLICATE KEY UPDATE status = '{}', version = '{}', executedAt=CURRENT_TIMESTAMP;
            """
        self.execute_query(sql.format(self.revision_table, filename, version, status, status, version))


    def rollback_migration(self, sql, id):
        try:
            self.execute_query(sql)
            self.remove_migration(id)
        except Error as e:
            raise e


    def remove_migration(self, id):
        sql = "DELETE FROM {} WHERE id = {} ;"
        return self.execute_query(sql.format(self.revision_table, id))


    def get_table_definition(self, tablename):
        return self.select_query("SHOW CREATE TABLE {}".format(tablename))


    def get_latest_db_revision(self):
        """ returns """
        sql = "SELECT * from {} ORDER BY id DESC LIMIT 1;"
        return self.select_query(sql.format(self.revision_table))


    def get_migrations_at_revision(self, version):
        sql = """ SELECT * FROM {} WHERE version = '{}' ORDER  BY id desc"""
        return self.select_query(sql.format(self.revision_table, version))

    def get_migrations_more_than_revision(self, version):
        sql = """ SELECT * FROM {} WHERE scheduledAt > (SELECT scheduledAt FROM {} WHERE version = '{}' ORDER  BY id desc LIMIT 1) ORDER BY id DESC; """
        return self.select_query(sql.format(self.revision_table,self.revision_table, version))