#!/usr/bin/env python
# -*- coding: utf-8 -*-

#TODO: Add user selection interface (/default user setting?)

from flask import Flask, request, render_template, Markup, redirect
# from hashlib import sha256
import MySQLdb
from enum import Enum
import sys

app = Flask(__name__)

class Location(Enum):
    local = 1
    pythonanywhere = 2
    unknown = 3


class Language(Enum):
    English = 1
    Hebrew = 2


def determine_location():
    if (50725104 == sys.hexversion):
        return Location.pythonanywhere
    if (50726640 == sys.hexversion):
        return Location.local
    return Location.unknown

app_location = determine_location()
app_language = Language.Hebrew

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
    res = "Hello World!<br />Did you mean to go to<a href='http://127.0.0.1:5000/web2'>http://127.0.0.1:5000/web2</a>?<br />" + sys.version + "<br />sys.hexversion = " + str(sys.hexversion) + "<br />Location determined = " + determine_location().name
    return res

@app.route("/show/", methods=["GET", "POST"])
def show():
    result = ""

    # Select data from table using SQL query.
    select_query = "SELECT \
                        expenses.idexpenses,\
                        expenses.name,\
                        expenses.amount,\
                        expenses.paid,\
                        expenses.payment_method,\
                        expenses.category,\
                        payment_methods.name,\
                        categories.idcategories,\
                        categories.name\
                    FROM \
                        expenses \
                        LEFT JOIN \
                        payment_methods \
                        ON \
                        expenses.payment_method = payment_methods.idpayment_methods \
                        LEFT JOIN \
                        categories \
                        ON \
                        expenses.category = categories.idcategories"
    if request.args.get('showall'):
        select_query += ";"
    else:
        select_query += " WHERE deleted = 0;;"

    cur = deb_execute_query(db, select_query)

    # print the first and second columns
    for row in cur.fetchall():
        result += "<div class=\"row\">" + \
                    "<div class=\"col-sm-4\" data-toggle=\"tooltip\" title='" + str(row[8]) + "'>" + str(row[1]) + "</div>" \
                    "<div class=\"col-sm-2\">" + str(row[2]) + "₪</div>" \
                    "<div class=\"col-sm-2\">" + str(row[6]) + "</div>" \
                    "<div class=\"col-sm-2\">" + str(row[3]) + "</div>" \
                    "<div class=\"col-sm-2\"><form action=\"/soft_delete/\" method = \"GET\"><input type='submit' class='btn btn-success' value='הסרה'><input type='hidden' name='id' value=" + str(row[0]) + "></input></form></div>" \
                  "</div>"
    return result

@app.route("/add/", methods=["GET", "POST"])
def add():
    #Input validation
    num_to_add = request.args.get('quantity')
    description_to_add = request.args.get('desc')
    payment_method_id = request.args.get('payment_method')
    category_id = request.args.get('category')
    if (not num_to_add.isnumeric()
        or not payment_method_id.isnumeric()
            or not category_id.isnumeric()):
        return

    user_id = '1';
    #INSERT INTO `affluence_schema`.`expenses` (`name`, `amount`, `paid`, `last_updated`, `payment_method`, `category`, `notes`, `deleted`) VALUES ('סנפלינג כיפי', '150', NOW(), NOW(), '4', '3', NULL, '0');
    insert_query = "INSERT INTO `expenses` (`user`, `name`, `amount`, `paid`, `last_updated`, `payment_method`, `category`) VALUES   ('" + user_id + "', '" + description_to_add + "', '" + num_to_add + "', NOW(), NOW()," + str(payment_method_id) + ", " + str(category_id) + ");"

    deb_execute_query(db, insert_query, True)

    #return show()
    return redirect("/web2", code=302)

@app.route("/hard_remove/", methods=["GET", "POST"])
def hard_remove():

    delete_query = "DELETE FROM `expenses` WHERE `idclient_test` = " + request.args.get('id') + ";"
    deb_execute_query(db, delete_query, True)

    return show()

@app.route("/soft_delete/", methods=["GET", "POST"])
def soft_delete():

    update_query = "UPDATE `expenses` SET `deleted` = 1 WHERE `idexpenses` = " + request.args.get('id') + ";"
    deb_execute_query(db, update_query, True)

    return redirect("/web2", code=302)

@app.route("/sum/", methods=["GET", "POST"])
def sum():
    result = ""

    # Select SUM query
    sum_query = "SELECT SUM(amount) FROM `expenses` WHERE deleted = 0;"
    cur = deb_execute_query(db, sum_query)
    # print the first column
    for row in cur.fetchall():
        result += "<strong>" + str(row[0]) + "</strong><br />"
        sum_this_month = row[0]

    # Select monthly_budget query
    monbudg_query = "SELECT valuesettings FROM `settings` WHERE `namesettings` = 'monthly_budget'";
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
    pm_query = "SELECT idpayment_methods, name FROM `payment_methods`"
    cur = deb_execute_query(db, pm_query)

    res = "<select class=\"form-control\" id=\"payment_method\" name=\"payment_method\">"
    for row in cur.fetchall():
        res += "<option value='" + str(row[0]) + "'>" + str(row[1]) + "</option>"
    res += "</select>"
    return res

def db_select_categories():
    cat_query = "SELECT idcategories, name FROM `categories`"
    cur = deb_execute_query(db, cat_query)

    res = "<select class=\"form-control\" id=\"category\" name=\"category\">"
    for row in cur.fetchall():
        res += "<option value='" + str(row[0]) + "'>" + str(row[1]) + "</option>"
    res += "</select>"
    return res

@app.route("/web2")
def index():
    if (Language.Hebrew == app_language):
        return render_template("he/your_base.html", db_expenses=Markup(show()), db_sum=Markup(sum()), db_payment_methods=Markup(db_select_payment_methods()), db_categories=Markup(db_select_categories()))
    else:
        return render_template("en/your_base.html", db_expenses=Markup(show()))

if __name__ == "__main__":
    app.run()

#TODO: Find where to stick db.close() (if at all)