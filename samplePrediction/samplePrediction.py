#!/usr/bin/env python
# encoding:utf-8
#
# Copyright 2014-2016 Yoshihiro Tanaka
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

__Author__  =  "Yoshihiro Tanaka"
__date__    =  "2014-08-20"
__version__ =  "1.4.4"

u"""SVM_for_samples 検体データに機械学習による人種推定をさせるためのプログラム

　LAST_UPDATE = 2015-01-09

"""

from sklearn import cross_validation
from sklearn.cross_validation import LeaveOneOut, StratifiedKFold
from sklearn.svm import LinearSVC, SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.feature_selection import RFE, RFECV
from sklearn.externals import joblib
import numpy as np
import os, commands, sys, random, time
from datetime import date

from flask import render_template, url_for
from jinja2 import Environment, FileSystemLoader

# 学習データ
# [[a, b, c], [a, b, c], [a, b, c], ...]
# 正解情報
# [1, 2, 0, ...]
# 試験データ
# [a, b, c]

class FeatureExtraction:
    def Prediction(self, pCode, sha):
        print "start prediction"

        estimator = joblib.load("pkl/" + pCode + "_pkl/" + pCode) 
        classes = estimator.classes_

        gtDict = {}
        with open("dataset/" + pCode + "_genotypes.tsv") as f:
            for line in f:
                items = line.rstrip().split("\t")
                gtDict[items[0]] = [items[1], items[2]]

        ngDict   = {}
        infile = open('../uploads/' + sha, "r")
        tmpDict = {}
        line = infile.readline()
        while line:
            if line[0] == "#":
                pass
            else:
                items = line.rstrip().split("\t")
                if items[0] in gtDict:
                    allele = 0
                    for i in range(len(items[3])):
                        if   items[3][i] == gtDict[items[0]][0]:
                            allele += 1
                        elif items[3][i] == gtDict[items[0]][1]:
                            allele += 3
                    if len(items[3]) == 1:
                        if   allele == 1:
                            tmpDict[items[0]] = 0.0
                        elif allele == 3:
                            tmpDict[items[0]] = 1.0
                        else:
                            tmpDict[items[0]] = 3.0
                            ngDict[items[0]]  = "Genotype is not registered"
                    else:
                        if   allele == 4:
                            tmpDict[items[0]] = 2.0
                        elif allele == 2:
                            tmpDict[items[0]] = 0.0
                        elif allele == 6:
                            tmpDict[items[0]] = 1.0
                        else:
                            tmpDict[items[0]] = 3.0
                            ngDict[items[0]]  = "Genotype is not registered"
            line = infile.readline()

        testdata = []
        c = 0
        for ID in gtDict.keys():
            if ID in tmpDict:
                testdata.append(tmpDict[ID])
                ngDict[ID] = "Read"
                c += 1
            else:
                testdata.append(3.0)
                ngDict[ID] = "This SNP could not be found"

        warn = False
        if c == 0:
            warn = True

        predDict = {}
        prob = estimator.predict_proba(testdata)
        label_pred = estimator.predict(testdata)
        predDict["RESULT"] = label_pred[0]
        for i in range(len(classes)):
            predDict[classes[i]] = prob[0][i]
        return predDict, ngDict, warn

def samplePrediction(pCode, sha):
    fe = FeatureExtraction()
    return fe.Prediction(pCode, sha)

def createHTML(sha, spcDict, pcDict, ngDicts, warn):
    print "Start create html."
    env = Environment(loader = FileSystemLoader('./', encoding='utf-8'), autoescape = False)
    tmpl = env.get_template('presult_template.html')
    with open('../templates/presult/' + sha + '.html', 'w') as f:
        f.write(tmpl.render(
            spcDict = spcDict,
            pcDict  = {k.split(":")[0]:v for k, v in pcDict.items()},
            ngDict  = ngDicts,
            warn    = warn))

if __name__=='__main__':
    try:
        sha = sys.argv[1]
        print "Start spc prediction."
        spcDict, spcNgDict, spcWarn = samplePrediction("spc", sha)
        if spcWarn:
            pcWarn = True
            pcDict = pcNgDict = {}
        else:
            print "Start pc prediction."
            pCode = spcDict["RESULT"]
            pcDict, pcNgDict, pcWarn = samplePrediction(pCode.lower(), sha)
        createHTML(sha, spcDict, pcDict, {"spc": spcNgDict, "pc": pcNgDict}, [spcWarn, pcWarn])
    except Exception as e:
        print e
    os.system('rm ../uploads/*' + sha + '*')
