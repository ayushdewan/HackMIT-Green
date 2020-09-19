from flask import Flask, render_template, request
app = Flask(__name__)

import json
import os

import flask
from time import sleep


app = flask.Flask(__name__)
app.secret_key = "secret"

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/upload')
def upload():
    return render_template("upload.html")

@app.route('/user/<username>')
def show_dash(username):
    return render_template("dashboard.html", username=username)