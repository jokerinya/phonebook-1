from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Ankara06'
app.config['MYSQL_DATABASE_DB'] = 'clarusway'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

# execute the code only ONCE
drop_table="""
DROP TABLE IF EXISTS phonebook;
"""
phonebook_table="""
CREATE TABLE phonebook (
  id INT NOT NULL AUTO_INCREMENT,
  person varchar(50) NOT NULL,
  number varchar(50),
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
data="""
INSERT INTO phonebook(person, number)
VALUES
    ("Buddy Rich", "999999999999" ),
    ("Candido", "11111111111111"),
	  ("Charlie Byrd", "123456789");
"""

cursor.execute(drop_table)
cursor.execute(phonebook_table)
cursor.execute(data)








if __name__ == "__main__":
    app.run(debug=True)