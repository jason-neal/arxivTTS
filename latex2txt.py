#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
import re



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


def main():
    fname ="/home/jason/article2speech/trigger_solar_system_5R1.tex"
    print(fname)
    #text_filter(inputname)
    with open(fname, 'r') as f:
        data = ""
        readflag = False
        for i, line in enumerate(f):
            if line.startswith("\\title"):
                data += line[7:-2] + "\n"
            if line.startswith("\\author"):
                # match first author in []
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
                data += " By " + author + etal + "\n"
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
            
    print(data)
    ##########################  
    ########Filter out###########

    word_replace = {"Myr":"Mega years","mjup":"jupiter mass", " A ": " Angstroms ",
                    "exoplanet":"exo-planet","S/N":"Signal to noise", "Fig.":"Figure", "Eq.":"Equation", "Eqs.":"Equations"} # Angstroms needs fixing
    units = {r's\$\^{-2}\$':' per second squared',r's\$\^{-1}\$':' per second',"pc":" parsec", "µm":"micrometers","km":"kilometers"," nm ": " nanometer ", " cm ":" centimeters ", " m ":" meters "}
    

    symbols = {r"\$N\$":"N", r"\$\\sim\$":" around ", r"\M\$\_\\odot\$": " Solar mass ",r"R\$\_\\odot\$":" Solar radii ", "\$>\$":" over ", r"\\rm":""}
    #$^{60}$Fe   -> Iron 60
    elements = {r"\$\^\{60\}\$Fe":" Iron 60", r"\$\^\{26\}\$Al":"Aluminium 26"}
    # citations with ecta brackets [] are not yet removed
    citations = {r"\\emph{.*}":"EMPHTERM",r'\\cite{.*}':'XXX', r'\\citet{.*}':' CITET', r'\\citep{.*}':' CITEP',r"\\ref{.*}":""}
    spaces = {r"\\\,":" ", r'\~':' '}
    # char--char  -> char-char
    # number--number -> number to number
    letters = {r"\\mu":"mu",r"\\nu":"nu",r"\\pi":"pi"}
    merger = merge_dicts(units, word_replace,letters) 
    for key, val in elements.iteritems():
        data = re.sub(key, val, data)

    for key, val in symbols.iteritems():
        data = re.sub(key, val, data)

    for key, val in citations.iteritems():
        data = re.sub(key, val, data)

    for key, val in spaces.iteritems():
        data = re.sub(key, val, data)

    for key, val in merger.iteritems():
        data = re.sub(key, val, data)
    ################### save output
    output = "latex2txt_test.txt"
   
    with open(output, "w") as fo:
        fo.write(data)
    print('Saved to ' + output )


    #s = '234.4'
    #s = 'test1.test2(test3);'
    #s.replace(\^([^\.]))
    #print(s)



if __name__ == "__main__":
    main()