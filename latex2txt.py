#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
import re
import tarfile
#from os import subprocess
from list_regex import regex_sub
from Arxiv import findRefType, downloadSource


def get_axiv_src(arxivname):
    """export.arxiv.org/e-print/arxivname     # source location
    http://export.arxiv.org/abs/1510.06642    # abstract webpage
    http://export.arxiv.org/pdf/1510.06642v1  # the pdf
    # ability to take in any of these inputs could be good in future
    """
    ref = arxivname.split("/").pop()
    print("reference from arxivname", ref)
    Download_path = "TMP/"
    # download source for arxivname article to tmp folder
    Type, ref = findRefType(ref)
    tar = tarfile.open(Download_path+ref, mode="r")

    # extract and find .tex file
    texfile = [x for x in tar.getmembers() if ".tex" in x.name]
    if len(texfile) >1:
        print("More than one tex file found")

    filename = texfile[0].name
    tar.extractall(members=texfile)
    
    return filename 
    

def main():
    #fname ="Test_articles/trigger_solar_system_5R1.tex"
    #fname ="Test_articles/Trifonov_2015.tex"
    url = "http://arxiv.org/e-print/1512.01087"
    Download_path = "TMP/"
    fname = get_axiv_src(url)
    with open(fname, 'r') as f:
        data = ""
        readflag = False
        for i, line in enumerate(f):
            if line.startswith("\\title"):
                data += re.sub(r"\\title\[(.*)\]{(.*)}", r"\g<1> - \g<2>\n", line)
                #data += line[7:-2] + "\n"
            if line.startswith("\\author"):
                # match first author in []
                # beautifulsoup parseing like roboph?
                print(line)
                for j, char in enumerate(line):
                    if char == "&":
                        limit = j
                        etal = " et. al."
                        break
                    elif char == "]":
                        limit = j
                        etal = ""
                    elif i == len(line):
                        limit = -1
                        etal = ""
                author = line[8:limit-1]
                data += "By " + author + etal + "\n"
                if line.endswith("\\\\"):
                    # line continues may need something here
                    pass
            if line.startswith("$^{"):
                continue
            if line.startswith("\\begin{abstract}"):
                readflag = True
                continue
            if line.startswith("\\end{abstract}"):
                readflag = False
                continue          
            if line.startswith("\\section{"):
                data += "\n" + line[9:-2] + "\n"
                readflag = True
                continue
            if line.startswith("\\section*"):
                data += "\n" + line[10:-2] + "\n"
                readflag = True
                continue
            if line.startswith("\\label"):
                continue
            if line.startswith("\\begin{figure"):
                readflag = False
                continue
            if line.startswith("\\end{figure"):
                readflag = True
                continue
            if line.startswith("\\begin{equation"):
                readflag = False
            # print("skipping equation-handle later")
                continue
            if line.startswith("\\end{equation"):
                readflag = True
                continue
                pass
            if line.startswith("%"):
                # SKIPING Comments
                continue
            if line.startswith("\\bibliography"):
                continue
            if line.startswith("\\end{document"):
                continue
            if line.startswith("\\begin{table"):
                readflag = False
                continue
            if line.startswith("\\begin{table"):
                readflag = True
                continue
            if readflag:
                data += line
        # subsections

        # chapters for extension to other documents?     


    #print(data)
    
    data = regex_sub(data) # Regex latex substituions performed
    
    #print(data)

    # Save output to text to observe subsitions
    output = fname.split(".")
    output.pop()
    output = output[0] +".txt"
    
    with open(output, "w") as fo:
        fo.write(data)
    print('Saved to ' + output )

    # Currently saving to txt file so that it be read by a tts program
    # Ideally use something already implemented in python

if __name__ == "__main__":
    main()