#!/usr/bin/env python

from flask import Flask
app = Flask(__name__)

@app.route("/das/")
def das():
    return "DAS from Flask"

@app.route("/")
def hello():
    return "Hello World from Flask"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8212)
