#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Markup, redirect
# from hashlib import sha256
import MySQLdb

app = Flask(__name__)

app_language = "Hebrew" # "English"

db = MySQLdb.connect(   host="localhost",       # your host
                        user="root",            # username
                        passwd="mySqlDb6",      # password
                        db="import_schema",     # name of the database
                        charset="utf8")         # Show Hebrew correctly!!
db_table_name = "expenses";
settings_table_name = "settings";

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
        return "Error occurred: " + query
    return cur

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/show/", methods=["GET", "POST"])
def show():
    result = ""

    # Select data from table using SQL query.
    select_query = "SELECT idexpenses, name, amount, paid, category FROM  `" + db_table_name + "` ;" if request.args.get('showall') else "SELECT idexpenses, name, amount, paid, category FROM `" + db_table_name + "` WHERE deleted = 0;"
    cur = deb_execute_query(db, select_query)

    # print the first and second columns
    for row in cur.fetchall():
        result += "<form action=\"/soft_delete/\" method = \"GET\"><p>" + " " + str(row[1]) + "  /  " + str(row[2]) + "₪    @ " + str(row[3]) + " <input type='submit' class='btn btn-success' value='הסרה'> </p><input type='hidden' name='id' value=" + str(row[0]) + "></input></form>"

    return result

@app.route("/add/", methods=["GET", "POST"])
def add():
    #Input validation
    num_to_add = request.args.get('quantity')
    description_to_add = request.args.get('desc')
    if (not num_to_add.isnumeric()):
        return

    user_id = '1';
    insert_query = "INSERT INTO `" + db_table_name + "` (`user`, `name`, `amount`, `paid`, `last_updated`) VALUES   ('" + user_id + "', '" + description_to_add + "', '" + num_to_add + "', NOW(), NOW());"

    deb_execute_query(db, insert_query, True)

    #return show()
    return redirect("/web2", code=302)

@app.route("/hard_remove/", methods=["GET", "POST"])
def hard_remove():

    delete_query = "DELETE FROM `" + db_table_name + "` WHERE `idclient_test` = " + request.args.get('id') + ";"
    deb_execute_query(db, delete_query, True)

    return show()

@app.route("/soft_delete/", methods=["GET", "POST"])
def soft_delete():

    update_query = "UPDATE `" + db_table_name + "` SET `deleted` = 1 WHERE `idexpenses` = " + request.args.get('id') + ";"
    deb_execute_query(db, update_query, True)

    return redirect("/web2", code=302)

@app.route("/sum/", methods=["GET", "POST"])
def sum():
    result = ""

    # Select SUM query
    sum_query = "SELECT SUM(amount) FROM `" + db_table_name + "` WHERE deleted = 0;"
    cur = deb_execute_query(db, sum_query)
    # print the first column
    for row in cur.fetchall():
        result += "<strong>" + str(row[0]) + "</strong><br />"
        sum_this_month = row[0]

    # Select monthly_budget query
    monbudg_query = "SELECT valuesettings FROM `" + settings_table_name + "` WHERE `namesettings` = 'monthly_budget'";
    cur = deb_execute_query(db, monbudg_query)
    # print the first column
    for row in cur.fetchall():
        result += "<strong>העברת שפע רצויה: " + str(row[0]) + "</strong><br />"
        monthly_budget = row[0]

    # Show percentage calculation
    result += "<strong>אחוז מהרצוי: " + str(round(((sum_this_month / monthly_budget)*100), 2)) + "%</strong>"

    return result

@app.route("/web")
def index():
    return render_template("add_form.html")

@app.route("/web2")
def index2():
    if ("Hebrew" == app_language):
        return render_template("he/your_base.html", db_expenses=Markup(show()), db_sum=Markup(sum()))
    else:
        return render_template("en/your_base.html", db_expenses=Markup(show()))

if __name__ == "__main__":
    app.run()

#TODO: Find where to stick db.close() (if at all)