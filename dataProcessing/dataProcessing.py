#!/usr/bin/env python
# encoding:utf-8
#
# Copyright [2014] [Yoshihiro Tanaka]
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

__Author__  = "Yoshihiro Tanaka"
__date__    = "2014-12-04"
__version__ = "1.0.0 (Stable)"

def createList(flag):
    with open("dataProcessing/sample_population.tsv") as f:
        lines = f.readlines()

    cList = list(set([r.split("\t")[1] for r in lines]))
    country = {} 
    spcDict = {}
    for line in lines:
        items = line.split("\t")
        country[items[1]] = [items[2], items[3]]
        spcDict[items[1]] = items[2]
    if flag == 1:
        return cList
    if flag == 2:
        with open("dataProcessing/sort.txt") as f:
            lines = f.readlines()
        pcSort = spcSort = {}
        for line in lines:
            items = line.split()
            if '*' in items[0]:
                spcSort[items[0].lstrip('*')] = items[1]
            else:
                pcSort[items[0]] = items[1]
        return pcSort, spcSort, spcDict
    if flag == 3:
        return country

# dataDict = 
#         {
#             "Population Code":
#             { 
#                 "Genotype": Count, "Genotype": Count
#             }
#         }
def toList(data):
    cList = createList(1)
    dataDict = {}
    conDict  = {}
    setList = []
    dataList = data.split(";")
    for i in range(len(dataList)):
        setList.extend([r.split(":")[0] for r in dataList[i].split(",")])
        conDict[cList[i]] = dataList[i]
    setList = set(setList)

    for k, v in conDict.items():
        if k in cList:
            sps = {r.split(":")[0]: int(r.split(":")[1]) for r in v.split(",")}
            gtList = []
            for sp in setList:
                if sp in sps:
                    gtList.append(sps[sp])
                else:
                    gtList.append(0)
            dataDict[k] = gtList 
    return setList, dataDict

def toPer(dataDict):
    perDict = {}
    for k, gtList in dataDict.items():
        perDict[k] = [round((r/float(sum(gtList)))*100, 1) for r in gtList]
    return perDict

# spcDict = {
#             "Super Population Code": 
#                 ["Population Code", "Population Code"]
#             }
def changeSPC(flag, dataDict):
    pcSort, spcSort, spcDict   = createList(2)
    totalDict = {}
    for pc, gtList in dataDict.items():
        if spcDict[pc] not in totalDict:
            totalDict[spcDict[pc]] = []
        for i in range(len(gtList)):
            try:
                totalDict[spcDict[pc]][i] += int(gtList[i])
            except:
                totalDict[spcDict[pc]].append(0)
                totalDict[spcDict[pc]][i] += int(gtList[i])
    if flag == 1:
        totalList = []
        for key, value in totalDict.items():
            totalList.append([int(spcSort[key]), key, value])
        return totalList

    stackList = []
    for key, value in dataDict.items():
        stackList.append([int(pcSort[key]), key, value])
    return stackList

def setMarkers(dataDict):
    header = True
    with open("dataProcessing/latLng.tsv") as f:
        lines = f.readlines()
    markers = []
    for line in lines:
        if header:
            header = False
        else:
            items = line.rstrip().split("\t")
            tmp   = {}
            tmp["latLng"] = items[:-1]
            tmp["name"]   = items[-1]
            markers.append(tmp)

    perDict = toPer(dataDict)
    for marker in markers:
        if marker["name"] in perDict:
            marker["pie"] = perDict[marker["name"]]
    mValue = [list(r) for r in zip(*[r["pie"] for r in markers])]
    return [markers, mValue]

def links(id):
    linkDict = {}
    linkDict["dbSNP"] = "http://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?rs=" + str(id)
    linkDict["ensembl"] = "http://asia.ensembl.org/Homo_sapiens/Variation/Explore?source=dbSNP;v=rs" + str(id)
    linkDict["snpedia"] = "http://www.snpedia.com/index.php/Rs" + str(id)
    linkDict["opensnp"] = "https://opensnp.org/snps/rs" + str(id)
    return linkDict
