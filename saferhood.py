import requests
import subprocess
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def saferhood():
    return render_template("saferhood.html")

@app.route('/communities')
def communities():
    return render_template("communities.html")

@app.route('/face')
def face():
    # live_rec.run()
    cmd = ['python3', 'live_rec.py']
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                              stderr = subprocess.PIPE,
                              stdin=subprocess.PIPE)
    out, err = p.communicate()
    return "direct your attention to the video feed!"


if __name__ == '__main__':
    app.run()
