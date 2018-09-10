from flask import Flask, request, render_template, Markup
# from hashlib import sha256
import MySQLdb

app = Flask(__name__)

app_language = "Hebrew" # "English"

db = MySQLdb.connect(host="yanoom.mysql.pythonanywhere-services.com",  # your host
                     user="yanoom",  # username
                     passwd="mySqlDb6",  # password
                     db="yanoom$affluence",  # name of the database
                     charset="utf8",    # Essential to display hebrew
                     use_unicode=True)  # Essential to display hebrew

def deb_execute_query(db, query, commit = False):
    # Create a Cursor object to execute queries.
    cur = db.cursor()

    # Select data from table using SQL query.
    try:
        cur.execute(query)
        if (commit):
            db.commit()
    except:
        if (commit):
            db.rollback()
        return "Error occured: " + query
    return cur

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/show/", methods=["GET", "POST"])
def show():
    result = ""

    # Select data from table using SQL query.
    select_query = "SELECT * FROM client_test" if request.args.get('showall') else "SELECT * FROM client_test WHERE deleted = 0"
    cur = deb_execute_query(db, select_query)

    # print the first and second columns
    for row in cur.fetchall():
        result += "<p>" + str(row[0]) + " " + row[1] + "</p>"

    sum_query = "SELECT SUM(data) FROM import_schema.client_test;"
    cur = deb_execute_query(db, sum_query)
    # print the first column
    for row in cur.fetchall():
        result += "<strong>" + str(row[0]) + "</strong>"

    db.close()
    return result

@app.route("/add/", methods=["GET", "POST"])
def add():
    insert_query = "INSERT INTO `import_schema`.`client_test` (`data`) VALUES ('" + request.args.get('num') + "');"
    deb_execute_query(db, insert_query)

    db.close()
    return show()

@app.route("/hard_remove/", methods=["GET", "POST"])
def hard_remove():

    delete_query = "DELETE FROM `import_schema`.`client_test` WHERE `idclient_test` = " + request.args.get('id') + ";"
    deb_execute_query(db, delete_query, True)

    db.close()
    return show()

@app.route("/soft_delete/", methods=["GET", "POST"])
def soft_delete():

    update_query = "UPDATE`import_schema`.`client_test` SET `deleted` = 1 WHERE `idclient_test` = " + request.args.get('id') + ";"
    deb_execute_query(db, update_query, True)

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

#if __name__ == "__main__":
#    app.run()