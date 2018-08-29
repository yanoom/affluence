from flask import Flask, request, render_template, Markup
# from hashlib import sha256
import MySQLdb

app = Flask(__name__)

app_language = "Hebrew" # "English"

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/show/", methods=["GET", "POST"])
def show():
    result = ""

    db = MySQLdb.connect(host="localhost",  # your host
                     user="root",  # username
                     passwd="mySqlDb6",  # password
                     db="import_schema")  # name of the database

    # Create a Cursor object to execute queries.
    cur = db.cursor()

    # Select data from table using SQL query.
    select_query = "SELECT * FROM client_test" if request.args.get('showall') else "SELECT * FROM client_test WHERE deleted = 0"
    try:
        cur.execute(select_query)
    except:
        return "Error occured: " + select_query

    # print the first and second columns
    for row in cur.fetchall():
        result += "<p>" + str(row[0]) + " " + row[1] + "</p>"

    db.close()
    return result

@app.route("/add/", methods=["GET", "POST"])
def add():

    db = MySQLdb.connect(host="localhost",  # your host
                     user="root",  # username
                     passwd="mySqlDb6",  # password
                     db="import_schema")  # name of the database

    # Create a Cursor object to execute queries.
    cur = db.cursor()

    insert_query = "INSERT INTO `import_schema`.`client_test` (`data`) VALUES ('" + request.args.get('num') + "');"
    try:
        cur.execute(insert_query)
        db.commit()
    except:
        db.rollback()
        return "Error occured:" + insert_query

    db.close()
    return show()

@app.route("/hard_remove/", methods=["GET", "POST"])
def hard_remove():

    db = MySQLdb.connect(host="localhost",  # your host
                     user="root",  # username
                     passwd="mySqlDb6",  # password
                     db="import_schema")  # name of the database

    # Create a Cursor object to execute queries.
    cur = db.cursor()

    delete_query = "DELETE FROM `import_schema`.`client_test` WHERE `idclient_test` = " + request.args.get('id') + ";"
    try:
        cur.execute(delete_query)
        db.commit()
    except:
        db.rollback()
        return "Error occured:" + delete_query

    db.close()
    return show()

@app.route("/soft_delete/", methods=["GET", "POST"])
def soft_delete():

    db = MySQLdb.connect(host="localhost",  # your host
                     user="root",  # username
                     passwd="mySqlDb6",  # password
                     db="import_schema")  # name of the database

    # Create a Cursor object to execute queries.
    cur = db.cursor()

    update_query = "UPDATE`import_schema`.`client_test` SET `deleted` = 1 WHERE `idclient_test` = " + request.args.get('id') + ";"
    try:
        cur.execute(update_query)
        db.commit()
    except:
        db.rollback()
        return "Error occured:" + update_query

    db.close()
    return show()

@app.route("/sum/", methods=["GET", "POST"])
def sum():
    num = request.args.get('num')
    result = "Adding numbers: " + str(num)
#    result += "Checksum: " + str(num)
    return result

@app.route("/web")
def index():
    return render_template("add_form.html")

@app.route("/web2")
def index2():
    if ("Hebrew" == app_language):
        return render_template("he/your_base.html", db_expenses=Markup(show()))
    else:
        return render_template("en/your_base.html", db_expenses=Markup(show()))

if __name__ == "__main__":
    app.run()