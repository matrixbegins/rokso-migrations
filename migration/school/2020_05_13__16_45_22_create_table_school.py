apply_sql = """
CREATE TABLE school (
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
firstname VARCHAR(30) NOT NULL,
lastname VARCHAR(30) NOT NULL,
email VARCHAR(50),
reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
"""

rollback_sql = "DROP table school"

migrations = {
    "apply": apply_sql,
    "rollback": rollback_sql
}
