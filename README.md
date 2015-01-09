# 1000 Genomes Visualization

The repository contains a program of Web services using the SNP data of 1000 Genomes Project.

## Features
* focused on the difference of Genotype frequency by Ethnicity.

## Use library
* Python
    * Flask
    * MySQL.connector
* JavaScript
    * jQuery
    * jVectorMap
    * Highcharts

## Version (recommended)
* python 2.7.5
* flask 0.10.1
* MySQL.connector 1.2.2
* jQuery 1.11.0
* jVectorMap 1.2.2


## DataBase

### OverView
* Engine  : InnoDB
* Size    : 25.2GiB
* Column  : 85,639,460
* Encoding: utf-8

### Table design
```SQL
CREATE TABLE `main` (
  `chr` varchar(2) NOT NULL DEFAULT '',
  `pos` int(15) NOT NULL,
  `id` varchar(15) NOT NULL,
  `REF` tinytext NOT NULL,
  `ALT` tinytext NOT NULL,
  `info` text NOT NULL,
  KEY `id` (`id`),
  KEY `pos` (`pos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

### Example
Column | Content
-------| -------
chr    | 1
pos    | 10177
id     | .
REF    | A
ALT    | AC
info   | 1&#124;1:23,1&#124;0:29,0&#124;1:28,0&#124;0:33;1&#124;1:9,0&#124;1:34,1&#124;0:20,0&#124;0:31;1&#124;1:28,0&#124;1:15,1&#124;0:27,0&#124;0:16;0&#124;0:19,0&#124;1:30,1&#124;0:26,1&#124;1:10;1&#124;1:9,1&#124;0:37,0&#124;1:36,0&#124;0:17;1&#124;1:35,0&#124;1:19,1&#124;0:24,0&#124;0:7;1&#124;1:3,0&#124;1:21,1&#124;0:31,0&#124;0:36;0&#124;0:34,1&#124;0:23,0&#124;1:42,1&#124;1:8;1&#124;1:2,0&#124;1:15,1&#124;0:23,0&#124;0:21;1&#124;1:4,0&#124;1:26,1&#124;0:24,0&#124;0:45;1&#124;1:21,0&#124;1:39,1&#124;0:42,0&#124;0:5;0&#124;0:38,0&#124;1:28,1&#124;0:29,1&#124;1:4;1&#124;1:7,1&#124;0:36,0&#124;1:38,0&#124;0:18;0&#124;0:13,0&#124;1:43,1&#124;0:41,1&#124;1:11;1&#124;1:1,0&#124;1:38,1&#124;0:30,0&#124;0:34;0&#124;0:16,1&#124;0:30,0&#124;1:36,1&#124;1:20;1&#124;0:21,0&#124;1:22,0&#124;0:62;1&#124;1:30,0&#124;1:26,1&#124;0:28,0&#124;0:15;1&#124;1:12,0&#124;1:26,1&#124;0:30,0&#124;0:28;0&#124;0:19,0&#124;1:24,1&#124;0:40,1&#124;1:20;1&#124;1:8,1&#124;0:26,0&#124;1:28,0&#124;0:34;1&#124;0:19,0&#124;1:20,0&#124;0:25;1&#124;1:18,1&#124;0:32,0&#124;1:38,0&#124;0:14;1&#124;1:10,1&#124;0:16,0&#124;1:13,0&#124;0:54;0&#124;0:13,1&#124;0:40,0&#124;1:30,1&#124;1:21;1&#124;1:6,0&#124;1:24,1&#124;0:27,0&#124;0:47

### Directory structure

```
.
$B('(!(!(B LICENSE
$B('(!(!(B README.md
$B('(!(!(B app.py
$B('(!(!(B dataProcessing
$B("$(Q)")"(B $B('(!(!(B __init__.py
$B("$(Q)")"(B $B('(!(!(B dataProcessing.py
$B("$(Q)")"(B $B('(!(!(B latLng.tsv
$B("$(Q)")"(B $B('(!(!(B sample_population.tsv
$B("$(Q)")"(B $B(&(!(!(B sort.txt
$B('(!(!(B log
$B('(!(!(B samplePrediction
$B("$(Q)")"(B $B('(!(!(B README.md
$B("$(Q)")"(B $B('(!(!(B __init__.py
$B("$(Q)")"(B $B('(!(!(B check_deadlink.sh
$B("$(Q)")"(B $B('(!(!(B dataset
$B("$(Q)")"(B $B("$(Q)")"(B $B('(!(!(B afr_genotypes.tsv
$B("$(Q)")"(B $B("$(Q)")"(B $B('(!(!(B amr_genotypes.tsv
$B("$(Q)")"(B $B("$(Q)")"(B $B('(!(!(B asn_genotypes.tsv
$B("$(Q)")"(B $B("$(Q)")"(B $B('(!(!(B eur_genotypes.tsv
$B("$(Q)")"(B $B("$(Q)")"(B $B(&(!(!(B spc_genotypes.tsv
$B("$(Q)")"(B $B('(!(!(B pkl.tar.gz
$B("$(Q)")"(B $B('(!(!(B presult_template.html
$B("$(Q)")"(B $B(&(!(!(B samplePrediction.py
$B('(!(!(B static
$B("$(Q)")"(B $B('(!(!(B Chart.min.js
$B("$(Q)")"(B $B('(!(!(B check.js
$B("$(Q)")"(B $B('(!(!(B drawchart.js
$B("$(Q)")"(B $B('(!(!(B index
$B("$(Q)")"(B $B("$(Q)")"(B $B(&(!(!(B 1G_logo.png
$B("$(Q)")"(B $B('(!(!(B library_list.txt
$B("$(Q)")"(B $B('(!(!(B map.js
$B("$(Q)")"(B $B('(!(!(B pred
$B("$(Q)")"(B $B("$(Q)")"(B $B(&(!(!(B drawchart.js
$B("$(Q)")"(B $B('(!(!(B search.css
$B("$(Q)")"(B $B('(!(!(B style.css
$B("$(Q)")"(B $B(&(!(!(B usejq.js
$B('(!(!(B templates
$B("$(Q)")"(B $B('(!(!(B _formhelpers.html
$B("$(Q)")"(B $B('(!(!(B index.html
$B("$(Q)")"(B $B('(!(!(B pred.html
$B("$(Q)")"(B $B('(!(!(B presult
$B("$(Q)")"(B $B('(!(!(B result.html
$B("$(Q)")"(B $B(&(!(!(B wait.html
$B(&(!(!(B uploads
```
