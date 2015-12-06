#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
import re
import tarfile
import subprocess
#from os import subprocess
import pyttsx
from list_regex import regex_sub
from Arxiv import findRefType, downloadSource


def get_axiv_src(arxivname):
    """export.arxiv.org/e-print/arxivname     # source location
    http://export.arxiv.org/abs/1510.06642    # abstract webpage
    http://export.arxiv.org/pdf/1510.06642v1  # the pdf
    # ability to take in any of these inputs could be good in future
    """
    ref = arxivname.split("/").pop()
    if "arXiv" in ref:
    	ref = ref.split(":").pop()
    print("ArXiv reference =", ref)
    Download_path = "TMP/"
    # download source for arxivname article to tmp folder
    Type, ref = findRefType(ref)
    downloadSource(ref, Type, Download_path)  # download the data
    tar = tarfile.open(Download_path+ref, mode="r")
    
    # extract and find .tex file
    texfile = [x for x in tar.getmembers() if ".tex" in x.name]
    if len(texfile) >1:
        print("More than one tex file found")
    print(texfile)
    filename = texfile[0].name
    tar.extractall(members=texfile)
    
    return filename 

def get_label(line, label_dict):
    """ Get label from this line and add to the corresponding dict"""
    pass

def main():
    #fname ="Test_articles/trigger_solar_system_5R1.tex"
    #fname ="Test_articles/Trifonov_2015.tex"
    #url = "http://arxiv.org/e-print/1512.01087"
    saveText= True
    saveWave= True
    url = "arXiv:1512.00492"
    #url = "http://arxiv.org/abs/1512.00777"
    Download_path = "TMP/"
    fname = get_axiv_src(url)
    with open(fname, 'r') as f:
    	#Initalizing
        data = ""
        readflag = False
        authorflag = False
        figureflag = False
        equationflag = False
        alignflag = False
        for i, line in enumerate(f):
                        
            if line.startswith("%"): # SKIPING Comments
                continue
            if line.startswith("$^{"):
                continue
            
            if line.startswith("\\bibliography"):
                continue
            if line.startswith("\\end{document"):
                continue

            if line.startswith("\\begin{abstract}"):
                readflag = True
                continue
            if line.startswith("\\end{abstract}"):
                readflag = False
                continue        

            if line.startswith("\\title"):
            	titleline = re.sub(r"\\title\[(.*)\]\{(.*)\}", r"\g<1> - \g<2>\n", line)
            	titleline = re.sub(r"\\title\{(.*)\}", r"\g<1>\n", titleline)
                data += titleline
                #data += line[7:-2] + "\n"
            if line.startswith("\\author"):
                # match first author in []
                # can have multiple single authors
                # beautifulsoup parsing like roboph?
                limit = -1    # default to end of line
                etal = ""     # default to blank
                for j, char in enumerate(line):
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
                if authorflag:  # there has been a previous \author line
                    data += "and " + author + etal + "\n"     
                else:
                    data += "By " + author + etal + "\n"
                authorflag = True    # if author called multiple times
                        
            if line.startswith("\\begin{table"):
                readflag = False
                continue
            if line.startswith("\\end{table"):
                readflag = True
                continue

            if line.startswith("\\section"):
            	match = re.sub(r"\\section\*?{(.*?)}.*",r"\g<1>", line)
                data += "\n" + match + "\n"
                readflag = True
                if "\\label" in line:
                	#get_label(line, "section")
                	pass
                continue
                       
            if line.startswith("\\subsection"):
            	match = re.sub(r"\\subsection\*?{(.*?)}.*",r"\g<1>", line)
                data += "\n" + match + "\n"
               # data += "\n" + line[12:-2] + "\n"match
                readflag = True
                continue
                  
            if line.startswith("\\label"):
            	############ TO DO #################
            	# store labels in dicts with order number
            	label_val = re.sub(r"\\label\*?\{(.*?)\}.*", r"\g<1>", line)
            	#get_label(line, )
                continue
            
            if line.startswith("\\begin{figure"):
                readflag = False
                figureflag = True
                continue
            if line.startswith("\\end{figure"):
                readflag = True
                figureflag = False
                continue
            
            if line.startswith("\\begin{equation"):
                readflag = False
                equationflag = True
            # print("skipping equation-handle later")
                continue
            if line.startswith("\\end{equation"):
                readflag = True
                equationflag = False
                continue
            
            if line.startswith("\\begin{align"):
                readflag = False
                alignflag = True
            # print("skipping align-handle later")
                continue
            if line.startswith("\\end{align"):
                readflag = True
                alignflag = False
            	continue
            
            if readflag:
                data += line
        
        # chapters for extension to other documents?     

    data = regex_sub(data) # Regex latex substituions performed
    
    #if savetext:
    # Save output to text file
    output = fname.split(".")
    output.pop()
    output_txt = output[0] +".txt"
    output_wav = output[0] +".wav"
    with open(output_txt, "w") as fo:
       	fo.write(data)
    print('Saved to ' + output_txt )
    # Currently saving to txt file so that it be read by a tts program
    # Ideally use something already implemented in python
    if saveWave:   # tts
    	start = time.time()
    	subprocess.call(["text2wave " + output_txt + " -o " + output_wav], shell=True)
	    print("Finished saving to arXiv:" + ref + " to " + output_wav)
	    print("Time to save audio = " + str(time.time()-start) + " seconds")

	    ### Other tts methods to continue investigating in future
        
	    ###### Google TTS
	    #import GoogleTTS
		# GoogleTTS.audio_extract(input_text='tunnel snakes rule apparently', args = {'language':'en','output':'outputto.mp3'})
    	#.HTTP Error 503: Service Unavailable

        #####Pyvona

        ###### gtts Google TTS
        #from gtts import gTTS
		# Text = "This should be saved as a mp3"
		# tts = gTTS(text="Text", lang="en") 
		# tts.save("hello.mp3")

    	###### pyttsx
    	# engine = pyttsx.init()
    	# engine.say("Testing speach engine")
    	# engine.say(data)
    	# engine.runAndWait()
    	
    if not saveText:
		subprocess.call(["rm " + fname], shell=True) # remove text file


if __name__ == "__main__":
    main()