from flask import Flask, render_template, request

app = Flask(__name__)

# Phone book part
phone_book = {
    "A":2121314,
    "Adana": 2324555,
    "Zzzzz": 121344,
    "Adanali Riza": 123456
}

developer = "Jokerinya"


# Routings
# index page
@app.route("/", methods=["GET", "POST"])
def main():
    if request.method=="POST":
        keyword = request.form["username"].strip().title()
        persons = []
        for name, number in phone_book.items():
            if keyword in name:
                persons.append({"name" : name, "number": number})

        if len(persons) < 1:
            return render_template("index.html", developer_name=developer, no_result=True, keyword=keyword)
    
        return render_template("index.html", developer_name=developer, show_result=True ,no_result=False, keyword=keyword, persons=persons)
    else:
        return render_template("index.html", developer_name=developer, show_result=False)


# delete
@app.route("/delete",  methods = ["GET", "POST"])
def delete():
    if request.method == "POST":
        username=request.form["username"].strip().title()
        if username in phone_book.keys():
            del phone_book[username]
            return render_template("delete.html", developer_name=developer, not_valid=False,show_result=True, result="Record Deleted")
        return render_template("delete.html", developer_name=developer, not_valid=True, show_result=False, message=f"There is no record with '{username}'")
    else:
        return render_template("delete.html", developer_name=developer, not_valid=False,show_result=False)

# Update and Add
@app.route("/add-update", methods=["GET"])
def add_update_get():
    return render_template("add-update.html", developer_name=developer, action_name="Add or Update", not_valid=False, show_result=False)

@app.route("/add-update", methods=["POST"])
def add_update_post():
    username=request.form["username"].strip().title()
    phonenumber=request.form["phonenumber"].strip()
    if username.isalpha() and phonenumber.isnumeric():
        if username in phone_book.keys():
            result = "Record Updated"
        else:
            result = "Record Added"
        phone_book[username] = phonenumber
        return render_template("add-update.html", developer_name=developer, action_name="Add or Update", not_valid=False, show_result=True, result=result)
    else:
        if username=="":
            message="Invalid input: Name can not be empty"
        elif phonenumber=="":
            message="Invalid input: Phone number can not be empty"
        elif not username.isalpha():
            message="Invalid input: Name of person should be text"
        elif not phonenumber.isnumeric():
            message= "Invalid input: Phone number should be in numeric format"
        else:
            message=""
        return render_template("add-update.html", developer_name=developer, action_name="Add or Update", not_valid=True, show_result=False, message=message)

if __name__ == "__main__":
    app.run(debug=True)