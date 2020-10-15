# -*- coding: UTF-8 -*-

from flask import Flask, escape, request, render_template, send_from_directory, make_response
import requests, json
from datetime import datetime
from conf.odfapi import apilist
import os, sys

from flask_babel import Babel
from flask import g, session
from flask_session import Session
from babel.support import Translations

app = Flask(__name__)
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'locales'
babel = Babel(app)
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = './cache'
SESSION_FILE_THRESHOLD = 100
SESSION_FILE_MODE = 600
app.config.from_object(__name__)
Session(app)

@babel.localeselector
def get_locale():
    return session['lang']

@app.route('/selectLang/', methods=["GET", "POST"])
def selectLang():
    if request.args.get('lang'):
        lang = request.args.get("lang")
    else:
        return make_response('{}', 404)
    if lang not in ['en', 'zh_TW']:
        lang = 'zh_TW'
    session['lang'] = lang
    request.babel_translations = Translations.load('locales', [lang])
    return make_response('{}', 200)


@app.route('/')
def landing():
    if 'lang' not in session:
        session['lang'] = "zh_TW"
    return render_template('index.html')
    
@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/price')
def price():
    return render_template('price.html')

@app.route('/price_form')
def price_form():
    return render_template('price_HTML_Form.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/table')
def table():
    return render_template('tbl2sc.html')

#SA
@app.route('/sa_preview')
def sa_preview():
    return render_template('SinglePage/preview.html')

@app.route('/sa_converter')
def sa_converter():
    return render_template('SinglePage/converter.html')

@app.route('/sa_mergeodf')
def sa_mergeodf():
    return render_template('SinglePage/mergeodf.html')

@app.route('/tbl2sc', methods=["POST"])
def tbl2sc():
    content = request.form['content']
    data = {
        "title": "Pytest",
        "format" : "ods",
        "font" : "標楷體",
        "oddRowColor": "#666666",
        "content":content
    }
    res = requests.post(apilist['table2sc'], data=data)
    filename = "tbl2sc_result"
    if not os.path.exists('file'):
        os.mkdir('file')
    with open(f"file/{filename}.{data['format']}", 'wb') as f :
        f.write(res.content)
    return "success"

@app.route('/tbl2sc_result', methods=["GET", "POST"])
def tbl2sc_result():
    return render_template("result.html", link=f"tbl2sc_result.ods")


@app.route('/resume_result', methods=['POST', 'GET'])
def resume_result():
    api = request.form['apiname']
    jsonData = request.form['userinput好']
    res = requests.post(apilist[api],json=json.loads(jsonData))
    filename = api + str(datetime.now()).replace(' ','').replace(':','')
    if not os.path.exists('file'):
        os.mkdir('file')
    with open(f'file/{filename}.odt', 'wb') as f :
        f.write(res.content)
    return render_template('result.html', link=f'{filename}.odt')

@app.route('/price_result', methods=['POST', 'GET'])
def price_result():
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

@app.route('/price_html_result', methods=['POST', 'GET'])
def price_html_result():
    formData = request.form
    
    api = request.form['apiname']
    res = requests.post(apilist[api], data=formData)
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
    if not os.path.exists('cache'):
        os.mkdir('cache')
    app.run(host='0.0.0.0', port="80", debug=True)
