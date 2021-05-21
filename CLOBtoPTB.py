import re
import os
import pandas as pd

filepath = "/home/gunnar/Projects/corpora/CROWN-CLOB/CLOB_POS/"

tagDF = pd.read_csv("CLOBtoPTB.csv", usecols=[0, 1])
tagDict = {str(k[0]): str(k[1]) for k in tagDF.values.tolist()}
c7tags = [str(k[0]) for k in tagDF.values.tolist()]
tagDict["NULL"] = "SYM" #Keeps reading the NULL tag in the csv as a null value.

def getCleanLine(line):
    return line.rstrip()

#does the actual tag conversion, used in convertTags
def subTag(matchobj):
    subbed = tagDict[matchobj.group(1)]
    return "_"+subbed

def convertTags(line):
    nline = re.sub(r'_([\S]+)', subTag, line)
    return nline

# Concatenate multi-word tags like "even_CS21 though_CS22"
def concatAll(line):
    nline = line
    for tag in c7tags:
        tagre = re.escape(tag)
        nline = re.sub(r'\S+_('+tagre+r')([0-9])[0-9]@?\s.+?('+tagre+r')\2\2', concatAllSub, nline)
    return nline

def concatAllSub(matchobj):
    orig = matchobj.group(0)
    tag = matchobj.group(1)
    new = re.sub(r'_'+tag+'[0-9][0-9]@?', "", orig)
    new = re.sub(r'\s', '-', new)
    return new+'_'+tag

def mainStuff(origfname, newfname):
    with open(origfname, 'r') as f1, open(newfname, 'a') as f2:
        fixedtags = []
        for line in f1.readlines():
            nline = concatAll(line)
            fixedtags.append(convertTags(nline))
        for line in fixedtags:
            line2 = "{}\n".format(line)
            f2.write(line2.lstrip())

def multiFileHelper(folder, fextension, fxn, *fargs):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(fextension):
                fxn(os.path.join(root, file), os.path.join(root, r'/home/gunnar/Projects/corpora/CLOB-PTB-Tags/C-'+file), *fargs)

multiFileHelper(filepath, ".txt", mainStuff)
