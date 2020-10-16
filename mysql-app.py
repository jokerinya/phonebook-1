from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)
developer = "Jokerinya"

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

def find_person(keyword):
    query=f"SELECT person, number FROM phonebook WHERE person like '%{keyword}%';"
    cursor.execute(query)
    raw_result = cursor.fetchall()  # tuple type
    result = [{"name" : row[0], "number": row[1]} for row in raw_result]
    if not any(result):
        result = [{"name" : "Not Found", "number": "Not Found"}]
    return result

def find_one(keyword):
    query=f"SELECT id, person, number FROM phonebook WHERE person like '{keyword}';"
    cursor.execute(query)
    raw_result = cursor.fetchone()
    return raw_result  # tupple

def delete_person(keyword):
    result = find_one(keyword)
    if result == None:
        return f"There is no record with {keyword}, no record deleted."
    query=f"DELETE FROM phonebook WHERE id = {result[0]}"
    cursor.execute(query)
    return f"The record deleted, it was: {result[1]} -- {result[2]}."




# Routings
# index page
@app.route("/", methods=["GET", "POST"])
def main():
    if request.method=="POST":
        keyword = request.form["username"].strip().title()
        persons = find_person(keyword)
        return render_template("index.html", developer_name=developer, show_result=True ,no_result=False, keyword=keyword, persons=persons)
    else:
        return render_template("index.html", developer_name=developer, show_result=False)


# delete
@app.route("/delete",  methods = ["GET", "POST"])
def delete():
    if request.method == "POST":
        username=request.form["username"].strip().title()
        if username.isnumeric():
            return render_template("delete.html", developer_name=developer, not_valid=True, show_result=False, message=f"Username is cannot be numeric '{username}'")

        result = delete_person(username)

        return render_template("delete.html", developer_name=developer, not_valid=False,show_result=True, result=result)
    else:
        return render_template("delete.html", developer_name=developer, not_valid=False,show_result=False)


# add



if __name__ == "__main__":
    app.run(debug=True)