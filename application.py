from flask import Flask, render_template, request
app = Flask(__name__)

import functools
import json
import os

import flask
import pymysql.cursors
from time import sleep

import requests_oauthlib
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

FB_CLIENT_ID = "630669214555271"
FB_CLIENT_SECRET = "630669214555271"
FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
FB_SCOPE = ["email"]



# # Connect to the database
# connection = pymysql.connect(host='35.238.255.61',
#                              user='root',
#                              password='claimcart',
#                              db='claims',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)

# app = flask.Flask(__name__)
# app.secret_key = "secret"


@app.route('/')
def index():
	return render_template("login.html")

@app.route('/dashboard')
def dashboard():
	return render_template("dashboard.html")
    
@app.route('/list')
def list():
    sleep(10)
    pricesum = 0
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `*` FROM `items` WHERE `user`=%s"
        cursor.execute(sql, (getEmail(),))
        result = cursor.fetchall()
        for i in result:
            pricesum += i['quantity'] * i['price']
            i['price'] = "$%0.2f" % i['price']
    return render_template("dashboard.html", table=result, pricesum=("$%0.2f" % pricesum))

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
