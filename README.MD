# rokso-migrations

A NOT so simple database migrations utility for Mysql based database migration in python.

## Features

* Create your migrations simply with CLI.
* Suitable for large projects because we maintain migration files based on entity/table.
* Reverse engineer your migrations from existing database.
* Check database state like `git status`.

## Installation

**This is work in progress and the package is still not properly published.**


## Usage

To see what rokso can do:
```
➜  rokso-migrations git:(master) ✗ python rokso/rokso.py --help
Usage: rokso.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create        ➕ create a database migration.
  init          🚀 init your migration project. configures db connection
                parameters

  last-success  ⤵️  last successful migration version number
  migrate       ⤴️  Apply all outstanding migrations to database.
  remap         🔄 Reverse engineer your DB migrations from existing database.
  rollback      ⤵️  Rollback last applied migration
  status        ✅ checks the current state of database and pending migrations

```

### Setup
There are many ways to initiate your project.
To start create a directory where you want to create project

```
> mkdir mydbproject
> cd mydbproject
➜  mydbproject git:(master) ✗ python3 ../rokso/rokso.py init
Enter path to setup project: .
Enter database hostname : localhost
Enter database name : mydb
Enter database username : root
Enter database password:
working directory::  /var/www/projects/python/rokso-migrations/mydbproject
[*] Checking state of config file in CWD
[#] Generating required dir(s) if not exist
[*] Config file has been created
Connected to MySQL Server version  8.0.21

Executing>>
            CREATE TABLE IF NOT EXISTS rokso_db_version (
                id INT auto_increment NOT NULL,
                filename varchar(255) NOT NULL,
                version varchar(100) NOT NULL,
                status VARCHAR(20) DEFAULT 'pending' NOT NULL,
                scheduledAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                executedAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT id_PK PRIMARY KEY (id),
                CONSTRAINT filename_UNQ UNIQUE KEY (filename)
            ) ENGINE=InnoDB;

query completed successfully..
>> Time taken: 0.0197secs
```
The above command does following things:
- Creates a directory `migration` under the project directory. This directory holds the migration sqls for database.
- Creates a file `config.json` which holds the connection string to Database.
- Creates a version control table `rokso_db_version` in the database.

Check all contents now
```
➜  mydbproject git:(master) ✗ ll
total 8
-rw-r--r--  1 user  staff   157B Sep 13 04:26 config.json
drwxr-xr-x  2 user  staff    64B Sep 13 04:26 migration

```

Check the table in database

```
mysql> desc rokso_db_version;
+-------------+--------------+------+-----+-------------------+-------------------+
| Field       | Type         | Null | Key | Default           | Extra             |
+-------------+--------------+------+-----+-------------------+-------------------+
| id          | int          | NO   | PRI | NULL              | auto_increment    |
| filename    | varchar(255) | NO   | UNI | NULL              |                   |
| version     | varchar(100) | NO   |     | NULL              |                   |
| status      | varchar(20)  | NO   |     | pending           |                   |
| scheduledAt | timestamp    | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| executedAt  | timestamp    | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+-------------+--------------+------+-----+-------------------+-------------------+
6 rows in set (0.00 sec)

```

Now we are ready for creating our new migrations

### Create migrations
To create a new migration run following command:

```
➜  mydbproject git:(master) ✗ python3 ../rokso/rokso.py create
Enter table/procedure/function name that you want to create this migration for.: website_customers
Enter a file name for this migration.: website_customers_table
creating a migration ...........
working directory::  /var/www/projects/python/rokso-migrations/mydbproject
[*] migration file 2020_09_13__04_39_48_website_customers_table.py has been generated
```
Now you can see a new file under migration directory has been generated:
```
➜  mydbproject git:(master) ✗ ll migration
total 0
drwxr-xr-x  3 user  staff    96B Sep 13 04:41 website_customers

➜  mydbproject git:(master) ✗ ll migration/website_customers
total 8
-rw-r--r--  1 user  staff   171B Sep 13 04:39 2020_09_13__04_39_48_website_customers_table.py

➜  mydbproject git:(master) ✗ cat migration/website_customers/2020_09_13__04_39_48_website_customers_table.py
apply_sql = """
WRITE your DDL/DML query here
"""

rollback_sql = "WRITE your ROLLBACK query here."

migrations = {
    "apply": apply_sql,
    "rollback": rollback_sql
}

```

Now you can edit this file and add the DDL/INSERTS/UPDATES in `apply_sql` and its extremely important to write `rollback_sql`. However if you do not want a rollback statement then leave the `rollback_sql` empty and Rokso will not report an error while executing or rolling back migrations.


### Apply/Run migrations


### Rollback migrations


### Reverse engineer your migrations

