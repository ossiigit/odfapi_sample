# -*- coding: UTF-8 -*-

from flask import Flask, escape, request, render_template, send_from_directory
import requests, json
from datetime import datetime
app = Flask(__name__)
apilist={
    '履歷表生成範例':'http://192.168.3.186:9980/lool/merge-to/10db8056-a485-11e9-8e17-080027f6714d',
    '報價單生成範例':'http://192.168.3.186:9980/lool/merge-to/1c934f06-a48c-11e9-8e17-080027f6714d',
    'salary':'',
}
@app.route('/')
def landing():
    return render_template('index.html')
    
@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/price')
def price():
    return render_template('price.html')

@app.route('/salary')
def salary():
    return render_template('salary.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    api = request.form['apiname']
    jsonData = request.form['userinput好']
    res = requests.post(apilist[api],json=json.loads(jsonData))
    filename = api + str(datetime.now()).replace(' ','').replace(':','')
    with open(f'file/{filename}.odt', 'wb') as f :
        f.write(res.content)
    return render_template('result.html', link=f'{filename}.odt')

@app.route('/download/<path:filename>', methods=['POST', 'GET'])
def download(filename):
    return send_from_directory(directory='file', filename=filename)

if __name__ == "__main__":
    app.run(port="80", debug=True)