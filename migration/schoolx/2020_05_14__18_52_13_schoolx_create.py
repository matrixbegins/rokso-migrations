apply_sql = """
CREATE TABLE schoolx (
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
firstname VARCHAR(30) NOT NULL,
lastname VARCHAR(30) NOT NULL,
email VARCHAR(50),
reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
"""

rollback_sql = "DROP table schoolx"

migrations = {
    "apply": apply_sql,
    "rollback": rollback_sql
}
