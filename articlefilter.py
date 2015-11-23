#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

## Article filter for turning pdf journal articles into speach or wave files.

## Filter a textfile to remove anomalies that don't need to be spoken

import subprocess
import re

def manage_filenames(pdffilename):
    filestruct = pdffilename.slit('/')
    if len(filestruct) is 1:
        pdfpath = ""
        pdfname = filestruct
    else:
        pdfname = filestruct.pop()
        pdfpath = filestruct.join("/")
    return pdfpath, pdfname

def extract_text(filename):
    """ Run command line code pdftohtml"""
    """  pdftohtml [options] <PDF-file> [<HTML-file> <XML-file>]
    -s output as single page, -i ignore images
    """
    #infile = filename + '.pdf'
    #testreplace = infile

    outputfile = filename.replace('.pdf','.txt')
    outputfile = outputfile.split("/").pop()
    outputfile = "orig_text/" + outputfile
    subprocess.call(['pdftotxt', filename, outputfile])
    return outputfile

def save_filtered_text(filename, txtdata):
    pass


def create_audio(filename, ext='.mp3'):
    """ Run the command tool txt2wave """
    outfilename = filename.split("/").pop()
    outfilename = "output/" + outfilename.replace('.txt', ext)
    #subprocess.call()
    #tesxt2wave ( filename, outfilename)

    print("Pdf convereted to {} file".format([ext, outfilename]))

def text_filter(filename):
    # load 
    with open(filename) as f:
        textdata = f.read()
    print("printing Text data after loading in")
    print(repr(textdata))  # print with representation of whitespace
    #print "%r" % textdata 
    filtering(textdata)
    # save
    filteredfile = filename.split("/").pop()
    filteredfile = "filtered_txt/filtered_" + filteredfile
    return filteredfile
    
def main(fname):
    path, filename = manage_filenames(fname)
    extracted_file = extract_text(filename)
    filtered_file = textfilter(extactedfile)
    path2wavefile = create_audio(filtered_file)
    #Testing_filtering of smaller file.


def filtering(textdata):
    pass

def merge_dicts(*dict_args):
    '''
    Given any number of dics, shallow copy and merge into a new dict, 
    precedence goes to key value pairs in latter dicts.
    (From python 3.5 can just use z = {**x, **y})
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def filtertest():
    fname ="Test_articles/art_section.txt"
    fname ="Test_articles/retest.txt"
    print(fname)
    #text_filter(inputname)
    with open(fname, 'r') as f:
        textdata = f.read()
    print("printing Text data after loading in")
    #print(repr(textdata))
    # starting with simple test
    formatterdict = {"_":" ",":":" ","-":" ", "_":" ", 
                     "\n\n":"\n",  "/2":" "}
    word_replace = {"mjup":"jupiter mass", " A ": " Angstroms ",
                    "exoplanet":"exo-planet","S/N":"Signal to noise", "Fig.":"Figure", "Eq.":"Equation", "Eqs.":"Equations"} # Angstroms needs fixing
    distance = {"µm":"micrometers"," nm ": " nanometer ", " cm ":" centimeters ", " m ":" meters "}
    
    # au , r jup , r earht, r sun
    velocity = {"km/s ":"kilometers per second ", "cm/s ":"centimeters per second","m/s ":"meters per second "}
    acceleration = {}
    #mass  kg, g, mjup, msun 
    units_dict = merge_dicts(acceleration, velocity, distance)
    
    symbols_dict = {"@":" at ", "&":"and"}
    brackets = {">":" ","<":" ", "(":" ", ")":" ","[":" ","]":" "}
    #regular expression dicts
    reg_words = {}
    re_symbols = {'λ':'lambda','φ':'phi','⊙':' Sun','Γ':'Gamma','η':'eta','ν':'nu','µ ':'mu ','µ,':'mu,','=':'equals','˜':'tilda'}
    re_stupidthings ={'':'','':'','':'' } # May wish to use FF to remove extra titles


    #http://stackoverflow.com/questions/5658369/how-to-input-a-regex-in-string-replace-in-python
    regexp = {"\d+.\d+" :" point "}
    #formatterdict["_"] = " "
    #formatterdict["@"] = " at "
    #formatterdict["\n"] = " "

    #\xce\xbb   = lambda  λ
    #\xce\x93    = Capital Gamma  Γ
    #\xcf\x86   =  phi   φ
    # η
    #\xe2\x8a\x99 = sun symbol ⊙    
    textdata2 = textdata
    
    simple_filter_dict = merge_dicts(word_replace, units_dict, symbols_dict, re_symbols,re_stupidthings) 
    print("Filters used")
    print(simple_filter_dict)
    # for key, value in formatterdict.iteritems():
    #             textdata = textdata.replace(key, value)
    for key, val in simple_filter_dict.iteritems():
                textdata = textdata.replace(key, val) 
    for key, val in simple_filter_dict.iteritems():
                textdata2 = re.sub(key, val, textdata2)   
    #for key, value in regexp.iteritems():
    #            textdata = textdata.replace(key, value)    
    print("Filtered text")
    print(textdata)
    print(textdata2)
    # save to file
    
    fout = fname
    fout = fout.replace('.txt','_filtered.txt')
   
    with open(fout, "w") as fo:
        fo.write(textdata)
    print('saved to "filtered_' + fout + '"')

    print('Testing regualar expresstionS')
    
      


    # whole_text = ""
    # with open("tmptext.txt","r") as f:
    #     for line in f:
    #         line = line.lower()
    #         for key, value in formatterdict.iteritems():
    #             line = line.replace(key, value)
    #         for key, value in unit_replace.iteritems():
    #             line = line.replace(key, value)    
    #         for key, value in regexp.iteritems():
    #             line = line.replace(key, value)    
    #         print(line)
    #         whole_text = whole_text + line + "\n" 

    # print("file", f)
    # print("whole_text", whole_text)
    # # save output file
    # with open("filtered_text.txt","w") as f:
    #     f.write("Filtered text output \n")
    #     f.write(whole_text)



    # # test 2
    # f = open("tmptext.txt","r")
    # alltext = f.read()
    # print("All the text using f.read() \n ", alltext)
    # for key, value in formatterdict.iteritems():
    #     alltext = alltext.replace(key, value)
    # for key, value in unit_replace.iteritems():
    #     alltext = alltext.replace(key, value)    
    # for key, value in regexp.iteritems():
    #     alltext = alltext.replace(key, value)    
    # print("filtered alltext", alltext)



if __name__ == "__main__":
    # main(fname)
    filtertest()