# encoding:utf-8
#
#
#
__Author__  =  "CORDEA"
__date__    =  "2015-01-06"
__version__ =  "1.4.5"

u"""SVM_for_samples 検体データに機械学習による人種推定をさせるためのプログラム

　LAST_UPDATE = 2015-01-06

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
from mail.sendmail import *

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

        estimator = joblib.load("/xxx/samplePrediction/pkl/" + pCode + "_pkl/" + pCode) 
        classes = estimator.classes_

        gtDict = {}
        idList = []
        with open("/xxx/samplePrediction/genotypes.tsv") as f:
            for line in f:
                items = line.rstrip().split("\t")
                gtDict[items[0]] = [items[1], items[2]]

        with open("/xxx/samplePrediction/dataset/" + pCode + "_ids.txt") as f:
            for line in f:
                idList.append(line.rstrip())

        infile = open('/xxx/uploads/' + sha, "r")
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
                    else:
                        if   allele == 4:
                            tmpDict[items[0]] = 2.0
                        elif allele == 2:
                            tmpDict[items[0]] = 0.0
                        elif allele == 6:
                            tmpDict[items[0]] = 1.0
                        else:
                            tmpDict[items[0]] = 3.0
                else:
                    tmpDict[items[0]] = 3.0
            line = infile.readline()

        testdata = []
        for ID in idList:
            if ID in tmpDict:
                testdata.append(tmpDict[ID])
            else:
                print "err"

        predDict = {}
        prob = estimator.predict_proba(testdata)
        label_pred = estimator.predict(testdata)
        predDict["RESULT"] = label_pred[0]
        for i in range(len(classes)):
            predDict[classes[i]] = prob[0][i]
        return predDict

def samplePrediction(pCode, sha):
    fe = FeatureExtraction()
    return fe.Prediction(pCode, sha)

def createHTML(sha, spcDict, pcDict):
    env = Environment(loader = FileSystemLoader('/xxx/', encoding='utf-8'), autoescape = False)
    tmpl = env.get_template('presult_template.html')
    with open('/xxx/' + sha + '.html', 'w') as f:
        f.write(tmpl.render(
            spcDict = spcDict,
            pcDict  = {k.split(":")[0]:v for k, v in pcDict.items()}))

def mail(sha):
    with open('/xxx/uploads/' + sha + '.log') as f:
        mail = f.readline().rstrip()
    url = "http://xxx/presult/" + sha
    sendMail("process succeed", url, mail)

if __name__=='__main__':
    sha = sys.argv[1]
    spcDict = samplePrediction("spc", sha)
    pCode = spcDict["RESULT"]
    pcDict = samplePrediction(pCode.lower(), sha)
    createHTML(sha, spcDict, pcDict)
    mail(sha)
    os.system('rm *' + sha + '*')
