#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: Add insert interface from Telegram Bot (In progress)
# TODO: Add deletion confirmation (referene: https://m.facebook.com/nataly.atik)
# TODO: Add pie chart in the summary section: Total / expenses (divided to categories)

from flask import Flask, request, render_template, Markup, redirect
# from hashlib import sha256
import MySQLdb
from enum import Enum
import sys
import requests
import json
from affluence_safe_module import affluence_bot_id, db_pass

app = Flask(__name__)

class Location(Enum):
    local = 1
    pythonanywhere = 2
    unknown = 3


class Language(Enum):
    English = 1
    Hebrew = 2


def determine_location():
    pythonanywhere_locations = {
        "python3.6": 50725104,
        "python3.10": 50988528,
    }
    if (sys.hexversion in pythonanywhere_locations.values()):
        return Location.pythonanywhere
    if (50726640 == sys.hexversion):
        return Location.local
    return Location.unknown

app_location = determine_location()
app_language = Language.Hebrew
user_id = ""

def db_connect():
    if (Location.local == app_location):
        db = MySQLdb.connect(host="localhost",                                  # your host
                             user="root",                                       # username
                             passwd=db_pass,                                    # password
                             db="affluence_schema",                             # name of the database
                             charset="utf8",                                    # Essential to display hebrew
                             use_unicode=True)                                  # Essential to display hebrew
    elif (Location.pythonanywhere == app_location):
        db = MySQLdb.connect(host="yanoom.mysql.pythonanywhere-services.com",   # your host
                             user="yanoom",                                     # username
                             passwd=db_pass,                                    # password
                             db="yanoom$affluence",                             # name of the database
                             charset="utf8",                                    # Essential to display hebrew
                             use_unicode=True)                                  # Essential to display hebrew
    else:
        print("Affluence App determine_location Error: No app location specified, system halt!")
        sys.exit()

    return db

#initialy connect to db
db = db_connect()

def db_execute_query(query, commit = False):
    global db

    # Perform SQL query.
    try:
        # Create a Cursor object to execute queries.
        cur = db.cursor()

        cur.execute(query)
        if (commit):
            db.commit()
    except (AttributeError, MySQLdb.OperationalError) as e:
        if (commit):
            db.rollback()
        print("Error occurred: " + str(e) + " ; query = " + query)

        # Reconnect to db and try again
        db = db_connect()
        # Create a Cursor object to execute queries.
        cur = db.cursor()
        cur.execute(query)
        if (commit):
            db.commit()
    return cur

@app.route("/")
def hello():
    res = "Hello World!<br />Did you mean to go to<a href='http://127.0.0.1:5000/web2'>http://127.0.0.1:5000/web2</a>?<br />" + sys.version + "<br />sys.hexversion = " + str(sys.hexversion) + "<br />Location determined = " + determine_location().name
    res += "</br> current year = " + db_select_current_year()
    return res

def db_select_current_year():
    # Select data from table using SQL query.
    select_query = "SELECT YEAR(now());"
    cur = db_execute_query(select_query)

    # Debug AttributeError: 'str' object has no attribute 'fetchall' issue
    if isinstance(cur, str):
        print ("isinstance(cur, str) - " + cur)

    return str(cur.fetchone()).replace("(", "").replace(")", "").replace(",", "")   # fetchone returns a tuple (with parentheses and commas, remove then

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
                        expenses.category = categories.idcategories "
    if request.args.get('month'):
        select_query += "WHERE(paid between DATE_FORMAT(NOW(), '%Y-" + request.args.get('month') +"-01') AND (DATE_ADD(LAST_DAY('" + db_select_current_year() + "-" + request.args.get('month') + "-01'), INTERVAL 1 DAY)) )"
    else:
        select_query += "WHERE(paid between DATE_FORMAT(NOW(), '%Y-%m-01') AND NOW() )"
    if request.args.get('showall'):
        select_query += " ORDER BY last_updated DESC;"
    else:
        select_query += " AND (deleted = 0) ORDER BY last_updated DESC;"

    cur = db_execute_query(select_query)

    # Debug AttributeError: 'str' object has no attribute 'fetchall' issue
    if isinstance(cur, str):
        print ("isinstance(cur, str) - " + cur)


    # print the selected columns
    for row in cur.fetchall():
        result += "<div class=\"row\">" + \
                    "<div class=\"col-sm-4\" data-toggle=\"tooltip\" title='" + str(row[8]) + "'>" + str(row[1]) + "</div>" \
                    "<div class=\"col-sm-2\">" + str(row[2]) + "₪</div>" \
                    "<div class=\"col-sm-2\">" + str(row[6]) + "</div>" \
                    "<div class=\"col-sm-2\">" + str(row[3]) + "</div>" \
                    "<div class=\"col-sm-2\"><form action=\"/soft_delete/\" method = \"GET\"><input type='submit' class='btn btn-success' value='הסרה'><input type='hidden' name='id' value=" + str(row[0]) + "></input></form></div>" \
                  "</div>"
    return result

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def db_add_expense(amount, description, payment_method_id="NULL", category_id="NULL"):
    #Input validation
    if (not "NULL" == payment_method_id and not (payment_method_id.isnumeric())) \
            or (not "NULL" == category_id and not (category_id.isnumeric())) \
            or (not isFloat(amount)):
        return False

    #INSERT INTO `affluence_schema`.`expenses` (`name`, `amount`, `paid`, `last_updated`, `payment_method`, `category`, `notes`, `deleted`) VALUES ('סנפלינג כיפי', '150', NOW(), NOW(), '4', '3', NULL, '0');
    insert_query = "INSERT INTO `expenses` (`user`, `name`, `amount`, `paid`, `last_updated`, `payment_method`, `category`) VALUES ('" + user_id + "', '" + description + "', '" + amount + "', NOW(), NOW()," + str(payment_method_id) + ", " + str(category_id) + ");"

    db_execute_query(insert_query, True)
    return True

@app.route("/add/", methods=["GET", "POST"])
def add():
    num_to_add = request.args.get('quantity')
    description_to_add = request.args.get('desc')
    payment_method_id = request.args.get('payment_method')
    if ('0' == payment_method_id):
        payment_method_id = "NULL"
    category_id = request.args.get('category')
    if ('0' == category_id):
        category_id = "NULL"

    # Call ADD function
    if (db_add_expense(num_to_add, description_to_add, payment_method_id, category_id)):
        return redirect("/web2", code=302)  #return show()
    else:
        return redirect("/error", code=302)  #return error

@app.route("/hard_remove/", methods=["GET", "POST"])
def hard_remove():

    delete_query = "DELETE FROM `expenses` WHERE `idclient_test` = " + request.args.get('id') + ";"
    db_execute_query(delete_query, True)

    return show()

@app.route("/soft_delete/", methods=["GET", "POST"])
def soft_delete():

    update_query = "UPDATE `expenses` SET `deleted` = 1 WHERE `idexpenses` = " + request.args.get('id') + ";"
    db_execute_query(update_query, True)

    return redirect("/web2", code=302)

@app.route("/sum/", methods=["GET", "POST"])
def sum():
    result = ""

    # Select SUM query
    sum_query = "SELECT SUM(amount) FROM `expenses` "
    if request.args.get('month'):
        sum_query += "WHERE(paid between DATE_FORMAT(NOW(), '%Y-" + request.args.get('month') +"-01') AND (DATE_ADD(LAST_DAY('" + db_select_current_year() + "-" + request.args.get('month') + "-01'), INTERVAL 1 DAY)) )"
    else:
        sum_query += "WHERE(paid between DATE_FORMAT(NOW(), '%Y-%m-01') AND NOW() )"
    if request.args.get('showall'):
        sum_query += ";"
    else:
        sum_query += " AND (deleted = 0);"

    cur = db_execute_query(sum_query)
    # print the first column
    for row in cur.fetchall():
        result += "<strong>" + str(round(row[0], 2)) + "</strong><br />"
        sum_this_month = row[0]

    if (None == sum_this_month):
        return "<strong>אין הוצאות!</strong>"

    # Select monthly_budget query
    monbudg_query = "SELECT valuesettings FROM `settings` WHERE `namesettings` = 'monthly_budget'";
    cur = db_execute_query(monbudg_query)
    # print the first column
    for row in cur.fetchall():
        result += "<strong>העברת שפע רצויה: " + str(row[0]) + "</strong><br />"
        monthly_budget = row[0]

    # Show percentage calculation
    result += "<strong>אחוז מהרצוי: " + str(round(((sum_this_month / monthly_budget)*100), 2)) + "%</strong>"

    return result

@app.route("/from_tg", methods=["GET", "POST"])
def from_tg():
    #Get full HTTP request data
    msg = request.get_data().decode("utf-8")
    msg_json = json.loads(msg)
    msg_text = msg_json["message"]["text"]

    # send message to telegram api url
    url = "https://api.telegram.org/" + affluence_bot_id + "/sendMessage?chat_id=315909554&text=Received message from TG!\n"

    if (("+" in msg_text) and ("+" == msg_text[0]) and ("|" in msg_text) ):
        #url += "Full msg=" + requests.utils.quote(msg_json, safe='')
        url += "Only Text=" + requests.utils.quote(msg_json["message"]["text"], safe='') + "\n"
        url += "User=" + requests.utils.quote(msg_json["message"]["from"]["username"], safe='') + "\n"
        expense_text_amount = msg_text.split("|", 2)
        try:
            if (isinstance(expense_text_amount[0], str) and isinstance(expense_text_amount[1], float)):
                url += "expense_text = " + expense_text_amount[0]
                url += "\nexpense_amount = " + expense_text_amount[1]
            else:
                url += "Failed to parse incoming message. Failed to convert to 'text | amount' format\n"
                expense_text = expense_text_amount[0]
                expense_amount = float(expense_text_amount[1])
                url += "str(expense_text_amount[0]) = " + expense_text + "\nstr(expense_text_amount[1]) = " + str(expense_text_amount[1])
                url += "\nisinstance(expense_text, str) = " + str(isinstance(expense_text, str)) + "\nisinstance(float(expense_amount, float)) = " + str(isinstance(expense_amount, float))
        except TypeError as e:
            url += "Failed to parse incoming message. TypeError:" + str(e)
    else:
        url += "Failed to parse incoming message. Check syntax! (did you forget to start with a '+' or seperate __text__ and __amount__ with '|' ?\n"
        url += "Full msg=" + requests.utils.quote(request.get_data(), safe='')

    res = requests.get(url).content
    return res

@app.route("/send_to_tg", methods=["GET"])
def send_to_tg():
    # msg should be accepted as GET parameter
    msg = request.args.get('msg')

    # send message to telegram api url
    url = "https://api.telegram.org/" + affluence_bot_id + "/sendMessage?chat_id=315909554&text="
    url += requests.utils.quote(msg, safe='')
    res = requests.get(url).content
    return res

@app.route("/web")
def index2():
    return render_template("add_form.html")

def db_select_payment_methods():
    pm_query = "SELECT idpayment_methods, name FROM `payment_methods`"
    cur = db_execute_query(pm_query)

    res = "<select class=\"form-control\" id=\"payment_method\" name=\"payment_method\">"
    res += "<option value='0' selected>אמצעי תשלום (ללא)</option>"
    for row in cur.fetchall():
        res += "<option value='" + str(row[0]) + "'>" + str(row[1]) + "</option>"
    res += "</select>"
    return res

def db_select_categories():
    cat_query = "SELECT idcategories, name FROM `categories`"
    cur = db_execute_query(cat_query)

    res = "<select class=\"form-control\" id=\"category\" name=\"category\">"
    res += "<option value='0' selected>קטגוריה (ללא)</option>"
    for row in cur.fetchall():
        res += "<option value='" + str(row[0]) + "'>" + str(row[1]) + "</option>"
    res += "</select>"
    return res

@app.route("/error")
def error():
    return render_template("he/error.html")

@app.route("/web2")
def index():
    global user_id
    if (request.args.get('user')):
        user_id = request.args.get('user')
    else:
        user_id = '2';

    if (user_id == '1'):
        user1_selected = "selected"
    else:
        user1_selected = ""
    if (user_id == '2'):
        user2_selected = "selected"
    else:
        user2_selected = ""

    if (Language.Hebrew == app_language):
        return render_template("he/your_base.html", db_expenses=Markup(show()), db_sum=Markup(sum()), db_payment_methods=Markup(db_select_payment_methods()), db_categories=Markup(db_select_categories()), user1_selected=user1_selected, user2_selected=user2_selected)
    else:
        return render_template("en/your_base.html", db_expenses=Markup(show()))

@app.route("/debug")
def debug_route():
    global user_id
    resp = ""
    user_id = request.args.get('user') if (request.args.get('user')) else '2'
    num_to_add = request.args.get('quantity')
    description_to_add = request.args.get('desc')
    payment_method_id = request.args.get('payment_method')
    category_id = request.args.get('category')
    resp += f"user_id = {user_id}, num_to_add = {num_to_add}, description_to_add = {description_to_add}, payment_method_id = {payment_method_id}, category_id = {category_id}"
    if (not "NULL" == payment_method_id and not (payment_method_id.isnumeric())):
        resp += "<br /><br />(not NULL == payment_method_id and not (payment_method_id.isnumeric()))"
    if (not "NULL" == category_id and not (category_id.isnumeric())):
        resp += "<br /><br />(not NULL == category_id and not (category_id.isnumeric())"
    if (not isFloat(num_to_add)):
        resp += "<br /><br />(not isFloat(num_to_add))"

    return resp

if __name__ == "__main__":
    app.run()

#TODO: Find where to stick db.close() (if at all)
