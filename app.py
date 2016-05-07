#!/usr/bin/env python
# encoding:utf-8
#
# Copyright 2015-2016 Yoshihiro Tanaka
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__Author__ =  "Yoshihiro Tanaka"
__date__    = "2014-12-15"
__version__ = "1.0.4"

from flask import Flask, redirect, render_template, request, url_for, send_from_directory
from werkzeug import secure_filename
application = Flask(__name__)

from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, validators

import mysql.connector

from dataProcessing.dataProcessing import *
import os, hashlib, time, commands

class SearchForm(Form):
    rsid      = TextField('rs [Ex. 186143557]', [validators.Length(min=1, max=15)])
    chrom     = TextField('Chromosome [Ex. 1]', [validators.Length(min=1, max=2)])
    position  = TextField('Position [Ex. 1]', [validators.Length(min=1, max=15)])

class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None


@application.route("/", methods=['GET', 'POST'])
def index():
    mes = False
    mes = request.args.get('mes')
    form = SearchForm(request.form)
    if request.method == 'POST':
        if request.form['position'] and request.form['chrom']:
            if request.form['btn'] == 'Search by position and chromosome number':
                return redirect(url_for('result', chrom=form.chrom.data, pos=form.position.data))
        elif request.form['rsid']:
            if request.form['btn'] == 'Search by rsID':
                return redirect(url_for('result', rsid=form.rsid.data))

    return render_template('index.html', 
                            form = [form, mes])

@application.route("/result", methods=['GET', 'POST'])
def result():
    form = SearchForm(request.form)
    if request.method == 'POST':
        if request.form['rsid']:
            return redirect(url_for('result', rsid=form.rsid.data))

    dataDict = {}
    perDict  = {}
    chrom = request.args.getlist('chrom')
    rsid  = request.args.getlist('rsid')
    pos   = request.args.getlist('pos')

    idList = []
    if len(rsid) != 0:
        rsid = rsid[0]
        if "rs" not in rsid:
            rsid = "rs"+str(rsid)
        query = 'id="' + str(rsid) + '"'
    elif len(pos) != 0:
        if len(chrom) != 0:
            pos   = pos[0]
            chrom = chrom[0]
            query = 'pos="' + str(pos) + '" and ' + 'chr="' + str(chrom) + '"'

    err = 0
    try:
        conDict  = {}
        infoDict = {}
        cursor = connect.cursor(cursor_class=MySQLCursorDict)
        cursor.execute('select * from main where ' + query, ())
        rows = cursor.fetchall()[0]
        cursor.close()
        for k, v in rows.items():
            if k == "info":
                conStr = v
            else:
                infoDict[k] = v
        setList, dataDict  = toList(conStr)
        if "pos" in query:
            pingDict  = {}
        else:
            pingDict  = links(str(rsid))
        spcDict   = changeSPC(1, dataDict)
        stackList = changeSPC(2, dataDict)
    except Exception as e:
        print e
        return redirect(url_for('index', mes=True))

    markerList = setMarkers(dataDict)
    ref = infoDict["REF"]
    alt = infoDict["ALT"].split(",")

    alleles = []
    for gts in setList:
        allele = []
        gt = [int(r) for r in gts.split("|")]
        print gt
        for r in gt:
            if   r == 0:
                allele.append(ref)
            else:
                allele.append(alt[r-1])
        alleles.append("|".join(allele).encode('utf-8'))

    country = createList(3)

    return render_template("result.html",
                           items = [
                                    dataDict,
                                    alleles,
                                    country,
                                    markerList,
                                    stackList
                                   ],
                           form = form,
                           info = [
                                    infoDict,
                                    pingDict
                                   ],
                           spc  = spcDict)

@application.route("/pred", methods=['GET', 'POST'])
def prediction():
    return render_template('pred.html', err = -1)

@application.route("/upload", methods=['POST'])
def upload():
    data = request.files['data']
    form = SearchForm(request.form)
    if request.method == 'POST':
        if data and data.filename.split('.')[-1] in ['txt', 'TXT']:
            filename = secure_filename(data.filename)
            sha = hashlib.sha224(str(time.time())).hexdigest()
            filepath = "uploads/" + sha
            data.save(filepath)

            os.system('nohup python samplePrediction/samplePrediction.py "' + sha + '" 2>&1 > log/' + sha + '.log &')
            return redirect(url_for('.waitProcessing', sha = sha))
    return render_template('pred.html', err = 1)

@application.route('/wait')
def waitProcessing():
    sha = request.args['sha']
    ls = [r.rstrip(".html") for r in commands.getoutput('ls templates/presult/').split("\n")]
    if sha in ls:
        return redirect(url_for('.showResult', sha = sha))
    else:
        return render_template('wait.html', sha = sha)

@application.route('/presult/<sha>')
def showResult(sha):
    return render_template('presult/' + sha + '.html')

@application.route("/index")
def returnIndex():
    return redirect(url_for('index'))    

if __name__ == "__main__":
    connect = mysql.connector.connect(
        user     ='xxx',
        password ='xxx',
        host     ='127.0.0.1',
        database ='phase3',
        charset  ='utf8')
    application.run(host="xxx", debug=True)
