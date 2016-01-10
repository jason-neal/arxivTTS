#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import time
import tarfile
import subprocess
import argparse
#from os import subprocess
#import pyttsx
from list_regex import regex_sub
from Arxiv import findRefType, downloadSource
"""#!/usr/local/bin/python3"""

def get_axiv_src(arxivname):
    """export.arxiv.org/e-print/arxivname     # source location
    http://export.arxiv.org/abs/1510.06642    # abstract webpage
    http://export.arxiv.org/pdf/1510.06642v1.pdf  # the pdf
    # ability to take in any of these inputs could be good in future
    """
    ref = arxivname.split("/").pop()
    if "arXiv" in ref:
        ref = ref.split(":").pop()
    
    if ref.endswith(".pdf"):
    	ref = ref.replace(".pdf","")

    print("ArXiv reference =", ref)
    Download_path = "SRC/"
    # Download source for arxivname article to tmp folder
    Type, ref = findRefType(ref)
    downloadSource(ref, Type, Download_path)  # download the data
    tar = tarfile.open(Download_path + ref, mode="r")
    
    # extract and find .tex file
    texfile = [x for x in tar.getmembers() if ".tex" in x.name]
    if len(texfile) >1:
        print("More than one tex file found")
    print(texfile)
    filename = texfile[0].name
    tar.extractall(members=texfile)
    
    return filename, ref

def get_label(line, label_dict):
    """ Get label from this line and add to the corresponding dict"""
    pass

def _parser():
    """Take care of all the argparse stuff.

    :returns: the args
    """
    parser = argparse.ArgumentParser(description="Arxiv Text-To-Speach")
    parser.add_argument('arxivID', help='Arxiv Identifier')
    parser.add_argument('-o', '--output', default=False,
                        help='Output Filename',)
    parser.add_argument('-t', '--saveText', default=False,
                       help='Save the text file')
    parser.add_argument('-s', '--saveAudio', default=True,
                       help='Save the audiofile')
    parser.add_argument('-k','--keepSrc', default=False,
                       help='Keep source tar file')
    parser.add_argument('-l','--keepTex', default=False,
                       help='Keep the latex source file name.tex')
    parser.add_argument('-e', '--ext', default="mp3",
                       help='Audio output extension')
    parser.add_argument('-a','--autoplay', default=False,
                       help='Automatically start playing')
    parser.add_argument('-p','--player', default="mplayer",
                       help='Mediaplayer to use for autoplay')
    parser.add_argument('--options', default="",
                       help='Extra command line player options')

    args = parser.parse_args()
    return args

def main(arxivID, output=False, ext="mp3", player="mplayer", saveAudio=True, saveText=False, keepSrc=False, keepTex=False, autoplay=False, options=""):
    #fname ="Test_articles/trigger_solar_system_5R1.tex"
    #fname ="Test_articles/Trifonov_2015.tex"
    #url = "http://arxiv.org/e-print/1512.01087"
    #url = "arXiv:1512.00492"
    #url = "http://arxiv.org/abs/1512.00777"
    TMPDIR = "TMP"
    FINALDIR = "FINAL"
    if saveAudio == "0" or saveAudio == "False":
        saveAudio = False
    elif not saveAudio == False:
        saveAudio = True

    if keepSrc == "0" or keepSrc == "False":
        keepSrc = False
    elif not keepSrc == False:
        keepSrc = True

    if keepTex == "0" or keepTex == "False":
        keepTex = False
    elif not keepTex == False:
        keepTex = True

    if saveText == "0" or saveText == "False":
        saveText = False
    elif not saveText == False:
        saveText = True
    
    if autoplay == "0" or autoplay == "False":
        saveText = False
    elif not autoplay == False:
        autoplay = True

    valid_audio = ["wav","mp3"]
    if ext not in valid_audio:
    	print(ext + " is not a valid audio output type")
    	print("Valid audio types are", valid_audio)
    	raise(typeError)

    fname, srcname = get_axiv_src(arxivID)
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
    if not output:
        output = fname.split(".")
        output.pop()
        output_txt = output[0] +".txt"
        output_audio = output[0] +"."+ ext
    else:
        output_txt = output +".txt"
        output_audio = output +"."+ ext
    with open(output_txt, "w") as fo:
           fo.write(data)
    print('Saved to ' + output_txt )
    # Currently saving to txt file so that it be read by a tts program
    # Ideally use something already implemented in python
    if not saveAudio:
    	if autoplay:
    		print("Need txt2speach commandline code here for subprocess call")
    		subprocess.call("festival --tts {0}/{1} {2}".format(FINALDIR, output_txt, options), shell=True) # remove text file
    	else:
    		print("Not saving audio file or playing audio")
   
    else:   # tts
        start = time.time()
        print("Saving audio ...")
        subprocess.call("text2wave {0}/{1} -o {0}/{2}".format(FINALDIR, output_txt, output_audio), shell=True)
        print("Finished saving to arXiv:{2} to {0}/{1}".format(FINALDIR, output_audio, srcname))
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
        

    print("Cleaning up files...")

    if not keepSrc:
        subprocess.call("rm {0}/{1}".format(SRCDIR, srcname), shell=True) # remove tar source file
        print("Removed {0}/{1}".format(SRCDIR, srcname))

    if not keepTex:
        subprocess.call("rm {0}/{1}".format(FINALDIR, fname), shell=True) # remove text file
        print("Removed {0}/{1}".format(FINALDIR, fname))

    if not saveText:
        subprocess.call("rm {0}/{1}".format(FINALDIR, output_txt), shell=True) # remove text file
        print("Removed {0}/{1}".format(FINALDIR, output_txt))
          
    if autoplay:
            """ Playing audio file just created """
            # possibly need different calls depending on the players if they have different input params, i.e. for speed etc
            subprocess.call("{0} {1}/{2} {3}".format(player, FINALDIR, output_audio, options), shell=True)
        


if __name__ == "__main__":
    args = vars(_parser())
    arxivID = args.pop('arxivID')
    opts = {k: args[k] for k in args}

    main(arxivID, **opts)