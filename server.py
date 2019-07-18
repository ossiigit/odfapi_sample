# -*- coding: UTF-8 -*-

from flask import Flask, escape, request, render_template, send_from_directory
import requests, json
from datetime import datetime
from conf.odfapi import apilist
import os
app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('index.html')
    
@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/price')
def price():
    return render_template('price.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    api = request.form['apiname']
    jsonData = request.form['userinput好']
    res = requests.post(apilist[api],json=json.loads(jsonData))
    filename = api + str(datetime.now()).replace(' ','').replace(':','')
    if not os.path.exists('file'):
        os.mkdir('file')
    with open(f'file/{filename}.odt', 'wb') as f :
        f.write(res.content)
    return render_template('result.html', link=f'{filename}.odt')

@app.route('/result2', methods=['POST', 'GET'])
def result2():
    api = request.form['apiname']
    formData = dict(request.form)
    # 手動拆解群組資料指定給 JSON 報價單 API 的 項目變數 
    itemDict = {
        
    }
    jsonData={}
    for key in formData:
        if 'item' in key:
            keyList = key.split('-')
            if keyList[1] not in itemDict:
                itemDict[keyList[1]] = {}
            itemDict[keyList[1]][keyList[2]] = formData[key]
        else:
            jsonData[key] = formData[key]

    jsonData['項目']=[]
    totalPrice = 0
    for item in itemDict:
        jsonData['項目'].append(itemDict[item])
        totalPrice += int(itemDict[item]['小計'])
    jsonData['總計'] = totalPrice

    res = requests.post(apilist[api], json=jsonData)
    filename = api + str(datetime.now()).replace(' ','').replace(':','')
    if not os.path.exists('file'):
        os.mkdir('file')
    with open(f'file/{filename}.odt', 'wb') as f :
        f.write(res.content)
    return render_template('result.html', link=f'{filename}.odt')

@app.route('/download/<path:filename>', methods=['POST', 'GET'])
def download(filename):
    return send_from_directory(directory='file', filename=filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port="80", debug=False)