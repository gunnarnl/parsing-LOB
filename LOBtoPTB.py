import re
import os
import csv
import pandas as pd

#origfile = "D:/corpus-work/corpora/ICAME/TEXTS/LOBTAG/LOBTH_M.TXT"
#newfile = "D:/corpus-work/test5.txt"

filepath = "D:/corpus-work/corpora/ICAME/TEXTS/LOBTAG"

tagDF = pd.read_csv("LOBtoPTB.csv", usecols=[0, 1])
tagDict = {k[0]: k[1] for k in tagDF.values.tolist()}

def getCleanLine(line):
    return line[7:].rstrip()

#Manually finds infinitival have/do (labeled identically to present have/do)
def fixAux(line):
    pattern = r"_(MD|TO)\s+([a-zA-Z']+)_(HV|DO)"
    regex = re.compile(pattern)
    nline = regex.sub(r"_\1 \2_VB", line)
    return nline

#Inserts possessive tag separately on dummy genitive.
def insertPOS(line):
    nline = re.sub(r'_([\S]+)"', r'_\1', line) #strip off the ditto (") thing
    nline = re.sub(r'_(PP\$|WP\$R?) ', r'_\1O ', nline)
    nline = re.sub(r'_([A-Z]+)\$ ', r'_\1 s_POS ', nline)
    nline = re.sub(r'_(PP\$|WP\$R?)O ', r'_\1 ', nline)
    return nline

#gets appropriate ptb tag for sub
def subTag(matchobj):
    subbed = tagDict[matchobj.group(1)]
    return "_"+subbed

def replaceTags(line):
    nline = re.sub(r'_([\S]+)', subTag, line)
    return nline

def removeTags(line):
    pattern = r'_\S+'
    regex = re.compile(pattern)
    nline = regex.sub('', line)
    pattern2 = r'\\0'
    regex2 = re.compile(pattern2)
    nline = regex2.sub('', nline)
    pattern3 = r'\*\?[0-9]'
    regex3 = re.compile(pattern3)
    nline = regex3.sub('', nline)
    pattern4 = r"\*?\*'"
    regex4 = re.compile(pattern4)
    return regex4.sub('"', nline)

#Sentences begin with ^
def getSents(ctext, newfile):
    pattern = r'\^([^^]*)(?=\^|$)'
    regex = re.compile(pattern)
    for match in regex.finditer(ctext):
        stng = "{}\n".format(match.group(1))
        newfile.write(stng.lstrip())
        #print(stng.lstrip())

def getSents2(ctext):
    sents = []
    clinesString = " ".join(ctext)
    pattern = r'\^([^^]*)(?=\^|$)'
    regex = re.compile(pattern)
    for match in regex.finditer(clinesString):
        sents.append(match.group(1))
    return sents

def mainStuff(origfname, newfname):
    with open(origfname, 'r') as f1, open(newfname, 'a+') as f2:
        cleanlines = []
        for line in f1.readlines():
            cleanlines.append(getCleanLine(line))
        # notags = []
        # for line in cleanlines:
        #     notags.append(removeTags(line))

        sents = getSents2(cleanlines)

        auxfixlines = []
        for line in sents:
            auxfixlines.append(fixAux(line))

        posLines = []
        for line in auxfixlines:
            posLines.append(insertPOS(line))

        tagLines = []
        for line in posLines:
            tagLines.append(replaceTags(line))

        #clinesString = " ".join(tagLines)
        #getSents(clinesString, f2)
        for k in tagLines:
            f2.write(k+"\n")

def multiFileHelper(folder, fextension, fxn, *fargs):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(fextension):
                fxn(os.path.join(root, file), os.path.join(root, r'/cleanLOBTag/C'+file), *fargs)

#mainStuff(origfile, newfile)
multiFileHelper(filepath, ".TXT", mainStuff)
