#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Markup, redirect
# from hashlib import sha256
import MySQLdb
from enum import Enum
import sys

app = Flask(__name__)

class Location(Enum):
    local = 1
    pythonanywhere = 2

class Language(Enum):
    English = 1
    Hebrew = 2


app_location = Location.local
app_language = Language.Hebrew

db_table_name = "expenses";
settings_table_name = "settings";

if (Location.local == app_location):
    db = MySQLdb.connect(host="localhost",                                  # your host
                         user="root",                                       # username
                         passwd="mySqlDb6",                                 # password
                         db="affluence_schema",                             # name of the database
                         charset="utf8",                                    # Essential to display hebrew
                         use_unicode=True)                                  # Essential to display hebrew
elif (Location.pythonanywhere == app_location):
    db = MySQLdb.connect(host="yanoom.mysql.pythonanywhere-services.com",   # your host
                         user="yanoom",                                     # username
                         passwd="mySqlDb6",                                 # password
                         db="yanoom$affluence",                             # name of the database
                         charset="utf8",                                    # Essential to display hebrew
                         use_unicode=True)                                  # Essential to display hebrew
else:
    print("Error: No app location specified, system halt!")
    sys.exit()

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
    return "Hello World!<br />Did you mean to go to<a href='http://127.0.0.1:5000/web2'>http://127.0.0.1:5000/web2</a>?"

def translate_payment_method(id):
    if(1 == id):
        return "מזומן"
    if(2 == id):
        return "אשראי"
    return str(id)

@app.route("/show/", methods=["GET", "POST"])
def show():
    result = ""

    # Select data from table using SQL query.
    select_query = "SELECT idexpenses, name, amount, paid, payment_method, category FROM  `" + db_table_name + "` ;" if request.args.get('showall') else "SELECT idexpenses, name, amount, paid, payment_method, category FROM `" + db_table_name + "` WHERE deleted = 0;"
    cur = deb_execute_query(db, select_query)

    # print the first and second columns
    for row in cur.fetchall():
        result += "<div class=\"row\">" + \
                    "<div class=\"col-sm-2\">" + str(row[1]) + "</div>" \
                    "<div class=\"col-sm-2\">" + str(row[2]) + "₪</div>" \
                    "<div class=\"col-sm-2\">" + translate_payment_method(row[4]) + "</div>" \
                    "<div class=\"col-sm-2\">" + str(row[3]) + "</div>" \
                    "<div class=\"col-sm-2\"><form action=\"/soft_delete/\" method = \"GET\"><input type='submit' class='btn btn-success' value='הסרה'><input type='hidden' name='id' value=" + str(row[0]) + "></input></form></div>" \
                  "</div>"
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
def index2():
    return render_template("add_form.html")

def db_select_payment_methods():
    pm_str = "<select class=\"form-control\" id=\"payment_select\" name=\"payment_method\">"
    pm_str += "<option>מזומן</option>"
    pm_str += "<option>אשראי</option>"
    pm_str += "</select>"
    return pm_str

def db_select_categories():
    pm_str = "<select class=\"form-control\" id=\"category_select\" name=\"category\">"
    pm_str += "<option>כיף ותחביבים</option>"
    pm_str += "<option>קורסים וסדנאות</option>"
    pm_str += "</select>"
    return pm_str

@app.route("/web2")
def index():
    if (Language.Hebrew == app_language):
        return render_template("he/your_base.html", db_expenses=Markup(show()), db_sum=Markup(sum()), db_payment_methods=Markup(db_select_payment_methods()), db_categories=Markup(db_select_categories()))
    else:
        return render_template("en/your_base.html", db_expenses=Markup(show()))

if __name__ == "__main__":
    app.run()

#TODO: Find where to stick db.close() (if at all)