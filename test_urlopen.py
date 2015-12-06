#Test import from file

import requests
import tarfile
import StringIO
import re
from Arxiv import findRefType, downloadSource

#import io   # python 3
url_to_get = "http://arxiv.org/e-print/1512.01087"
# r = requests.get(url_to_get)
# print(r)
# print("ok ",r.ok)
# print("status code ",r.status_code)
# print("headers encoding ", r.headers['content-encoding'])
# print("headers type ", r.headers['content-type'])
# print("encoding ", r.encoding)
#print("text ", r.text)
#tarfile.open(r, mode="r")

#t = tarfile.open(fileobj=r, mode="r")

#print(t)
ref = "1512.01087"
Download_path = "TMP/"
# using arxiv 
Type, ref = findRefType(ref)
#d = downloadSource(ref, Type, Download_path)  # download the data


tar = tarfile.open(Download_path+ref, mode="r")

print("Members of tar", tar.getmembers())
a = [x for x in tar.getmembers() if ".tex" in x.name]
texfile = [x for x in tar.getmembers() if ".tex" in x.name]
print("tex file", texfile)
if len(texfile) >1:
	print("More than one tex file found")

filename = texfile[0].name
tar.extractall(members=texfile)
print(filename)

# load in file
with open(filename, 'r') as f:
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
                	print(j)
                    if char == "&":
                        limit = j
                        etal = " et. al."
                        break
                    elif char == "]":
                        limit = j
                        etal = ""
                    elif j == len(line):
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



