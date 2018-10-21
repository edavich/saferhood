import requests
import subprocess
from flask import Flask, request, render_template
app = Flask(__name__)

import requests
import base64
import json
import urllib.request

@app.route('/')
def saferhood():
    return render_template("saferhood.html")

@app.route('/communities')
def communities():
    return render_template("communities.html")



@app.route('/responders', methods=['GET', 'POST'])
def responders():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        language = request.form.get('language')
        img = urllib.request.urlretrieve(str(language), 'sample.jpg')

        IMAGE_PATH = 'sample.jpg'
        SECRET_KEY = 'sk_cbdbd5a608e152d5f6cb0975'

        with open(IMAGE_PATH, 'rb') as image_file:
            img_base64 = base64.b64encode(image_file.read())

        url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
        r = requests.post(url, data = img_base64)

        data = json.dumps(r.json(), indent=2)
        parsedData = json.loads(data)
        return render_template("responders.html",image=language,data=parsedData['results'][0]['plate'])
    return render_template("responders.html")

@app.route('/face')
def face():
    cmd = ['python3', 'live_rec.py']
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                              stderr = subprocess.PIPE,
                              stdin=subprocess.PIPE)
    out, err = p.communicate()
    return "surveillance";


if __name__ == '__main__':
    app.run()
