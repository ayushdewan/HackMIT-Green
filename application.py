from flask import Flask, render_template, request
app = Flask(__name__)

import json
import os
import subprocess

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


@app.route('/powerstat')
def powerstat():
    output = subprocess.Popen("sudo tlp-stat | grep -P '\[m(W|A)\]'", shell=True, stdout=subprocess.PIPE).stdout.read().decode("UTF-8")
    output = int(output[output.find("=") + 1: output.find("[")].strip())
    return output

