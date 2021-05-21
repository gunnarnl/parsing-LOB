# Converts original FLOB tags to PTB tags as in FLOBtoPTB.csv

import re
import os
import pandas as pd

filepath = "/home/gunnar/Projects/corpora/FLOB-POS/"

tagDF = pd.read_csv("FLOBtoPTB.csv", usecols=[0, 1])
tagDict = {k[0]: k[1] for k in tagDF.values.tolist()}

def getCleanLine(line):
    return line.rstrip()

#only remove excess (i.e. non-POS tags)
def removeTags(line):
    pattern = r'<[^<]*>'
    regex = re.compile(pattern)
    nline = regex.sub('', line)
    return nline

#does the actual tag conversion, used in convertTags
def subTag(matchobj):
    subbed = tagDict[matchobj.group(1)]
    return "_"+subbed

def convertTags(line):
    nline = re.sub(r'_([\S]+)', subTag, line)
    return nline

def cleanPTBTag(line):
    nline = re.sub(r'\s\]', ']', line)
    nline = re.sub(r'\s+(?=[^[\]]*\])', '-', nline)
    nline = re.sub(r'\[|\]', '', nline)
    return nline

def getTags(line):
    #Convert tags to non-xml format
    nline = re.sub(r"<[wc] ([A-Z0-9]+)>([^<]+) ?(?=<|$)", r"[\2]_\1 ", line)

    #remove excess tags
    notag = removeTags(nline)

    #convert tags to ptb
    convTag = convertTags(notag)

    #Removes junk
    cleanTag = cleanPTBTag(convTag)
    return cleanTag

#Sentences begin with <s
def getSents(ctext):
    sents = []
    pattern = r'(<s.*?)(?=<s|$)'
    regex = re.compile(pattern)
    for match in regex.finditer(ctext):
        sents.append(match.group(1))
    return sents
        #stng = "{}\n".format(match.group(1))
        #newfile.write(stng.lstrip())
        #print(stng.lstrip())

def mainStuff(origfname, newfname):
    with open(origfname, 'r') as f1, open(newfname, 'a') as f2:
        cleanlines = []
        for line in f1.readlines():
             cleanlines.append(getCleanLine(line))
        sents = getSents(" ".join(cleanlines))

        fixedtags = []
        for line in sents:
            fixedtags.append(getTags(line))
        for line in fixedtags:
            line2 = "{}\n".format(line)
            f2.write(line2.lstrip())

def multiFileHelper(folder, fextension, fxn, *fargs):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(fextension):
                fxn(os.path.join(root, file), os.path.join(root, r'/home/gunnar/Projects/corpora/FLOB-PTB-Tags/C-'+file), *fargs)

#mainStuff(testfile, newfile)
multiFileHelper(filepath, ".txt", mainStuff)
