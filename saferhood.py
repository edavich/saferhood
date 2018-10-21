import requests
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def saferhood():
    return render_template("saferhood.html")


if __name__ == '__main__':
    app.run()
