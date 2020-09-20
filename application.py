from flask import Flask, render_template, request
app = Flask(__name__)

import functools
import json
import os

import flask
from time import sleep
import pymysql.cursors

import requests_oauthlib
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

FB_CLIENT_ID = "630669214555271"
FB_CLIENT_SECRET = "630669214555271"
FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
FB_SCOPE = ["email"]



# # Connect to the database
connection = pymysql.connect(host='35.238.255.61',
                             user='root',
                             password='claimcart',
                             db='claims',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = flask.Flask(__name__)
app.secret_key = "secret"


@app.route('/')
def index():
	return render_template("login.html")

@app.route('/home')
def home():
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `*` FROM `board`"
        cursor.execute(sql)
        result = cursor.fetchall()
    for i in result:
        # i["carbon"] *= 7
        if i["name"] == "Ayush":
            i["hls"] = True
        else: 
            i["hls"] = False
        print(i["name"], i["hls"])
    return render_template("home.html", table=result)

@app.route('/dashboard')
def dashboard():
	return render_template("dashboard.html")
    
@app.route('/list')
def list():
    import psutil
    procs = {}
    # Iterate over all running processes
    for proc in psutil.process_iter():
        # Get process detail as dictionary
        pInfoDict = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
        p = psutil.Process(pInfoDict['pid'])
        # x = p.memory_info()[1]
        x = p.memory_percent(memtype="vms")
        if pInfoDict["name"] not in procs:
            procs[pInfoDict["name"]] = x
        else:
            procs[pInfoDict["name"]] += x

    lst = []
    for k in procs:
        lst.append((procs[k], k))
        lst.sort()
        lst = lst[::-1]

    exc = {"svchost.exe", "vmmem"}
    result = []
    process_id = 1
    total_usage = 0
    for i in lst:
        if i[1] not in exc:
            result.append({"id": process_id, "name": i[1], "bolts": i[0], "carbon": i[0]})
            process_id += 1
            total_usage += i[0]
            if process_id > 10:
                break

    for i in result:
        i['bolts'] = round(44 * i['bolts'] / total_usage, 2)
        i['carbon'] = round(87 * i['carbon'] / total_usage, 2)
    return render_template("dashboard.html", table=result)

@app.route('/family')
def family():
    pricesum = 0
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `*` FROM `items`"
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            pricesum += i['quantity'] * i['price']
            i['price'] = "$%0.2f" % i['price']
    return render_template("dashboard.html", table=result, pricesum=("$%0.2f" % pricesum))

@app.route('/updatedb', methods=['POST'])
def updatedb():
    with connection.cursor() as cursor:
        # Read a single record
        sql = "UPDATE `items` SET `user`=%s, `name`=%s, `quantity`=%s, `price`=%s, `description`=%s WHERE `item_id`=" + request.form["num"]
        cursor.execute(sql, (request.form["email"], request.form['name'], request.form['quantity'], request.form["price"].lstrip("$"), request.form["description"]))
    connection.commit()

    pricesum = 0
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `*` FROM `items`"
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            pricesum += i['quantity'] * i['price']
            i['price'] = "$%0.2f" % i['price']
    return render_template("dashboard.html", table=result, pricesum=("$%0.2f" % pricesum))


@app.route('/upload')
def upload():
    return render_template("upload.html")

@app.route('/user/<username>')
def show_dash(username):
    return render_template("dashboard.html", username=username)
