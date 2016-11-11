
""" Processing tex commands to words using regular expresions.

Edit these to include extra expressions as they are incountered """
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



def process_regexs(data, regexs):
    # Processing all dictionary regexs
    for key, val in regexs.iteritems():
        data = re.sub(key, val, data)
    
    return data
   



def do_sub(data):
    """ Substitue latex for words"""
    # Order not preserved in dict,
    # lists may be better for order presevation, 
    # would only need one list with the cleaning ones at the end.
    regexs = main_regex()
    clean = cleaning_regex()   
    data = process_regexs(data, regexs)
    data = process_regexs(data, clean)    
    return data
    
    # Junk to make still present issues stand out in txt file 
    #data = process_regexs(data, reveal())

def reveal():
    """ Identifying things to add 
    Only for testing purposes
    """
    
    Reveal = {r"\\(.*?){":"#### REVEALING \g<1> REVEALING ####"}

    return Reveal

def cleaning_regex():
    """ Regex for final things like removing $ and exra white spaces """
    
    clean = {r"\$(.*?)\$":r" \g<1> ", \
                r" +":" " \
                }

    return clean



def main_regex(): 
    """ Regex for replacement"""
    misc = {r" ?Myr ?":" Mega years ", \
            r" ?SNR ?":" signal to noise ratio ",\
            r" ?S/N ?":" Signal to noise ", \
            r'(\d+)\"':"\g<1> arcsecond", \
            } 

    units = {r"( |\\,)s\$?\^{-2}\$?":' per second squared', \
            r"( |\\,)s\$?\^{-1}\$?":' per second', \
            r" ([A-Za-z]+ ?)\$?\^{-2}\$?":r" per \g<1> squared ", \
            r"( .*[^A-Za-z])pc[^A-Za-z]":"\g<1> parsec ", \
            r"[^A-Za-z]\\?mu ?m[^A-Za-z] ?":r" micrometers ", \
            r"( .*[^A-Za-z])km[^A-Za-z]":"V kilometers ", \
            r"( .*[^A-Za-z])nm[^A-Za-z]":r"\g<1> nanometers ", \
            r"( |\\,)cm[^A-Za-z]":r"\g<1> centimeters ", \
            r"(\d+)( |\\,)m[^A-Za-z]":r"\g<1> meters ", \
            r"( .*[^A-Za-z])Hz[^A-Za-z]":r"\g<1> Hertz ", \
            r" ?\\AA ?":" Angstroms ", \
            }  # [^A-Za-z] not another letter before or after (i.e. can't match in a word)
    
    BodyUnits = {r"[^MR]\_\\oplus":" Earth ", \
               r"[^MR]\_\\odot":" Sun ", \
               r"[^MR]\_\\star":" Star ", \
               r"M ?\$?\_{?\\oplus}?\$?":" Earth masses ", \
               r"M ?\$?\_{?\\odot}?\$?": " Solar masses ", \
               r"M ?\$?\_{?\\star}?\$?": " Stellar masses ", \
               r"R ?\$?\_{?\\oplus}?\$?":" Earth radii ", \
               r"R ?\$?\_{?\\odot}?\$?":" Solar radii ", \
               r"R ?\$?\_{?\\star}?\$?":" Stellar radii ", \
               }
              
    #$^{60}$Fe   -> Iron 60
    elements = {r"\$\^\{60\}\$Fe":" Iron-60", \
                r"\$\^\{26\}\$Al":"Aluminium-26", \
                }

    # citations 
    # still have some issues with losing end brackets
    citations = {r'\\cite\*?{(.*?)}{1}':r" \g<1> ", \
                 r"\\citet\*?{(.*?)}{1}":r" \g<1> ", \
                 r"\\citep\*?\{(.*?)}{1}":r" ", \
                 r"\\cite[p]\*?\[(.*?)\]\[(.*)\]{(.*?)}?.?":r" ", \
                 r"\\ref{(.*)}":" \g<1> ", \
                 }
                 #r"\\cite[p]\*?\[(.*)\]\[(.*)\]{(.*)}":r" \g<1> \g<2>"

    set_space = {r"\\\,":" ", \
                 r"\~":r" ", \
                 }

    letters = {r"\\aplha":r" aplha ", \
               r"\\[b]eta":r" beta ", \
               r"\\[Gg]amma":r" gamma ", \
               r"\\[Dd]elta":r"delta", \
               r"\\[var]?epsilon":" epsilon ", \
               r"\\zeta":" zeta ", \
               r"\\eta":r" eta ", \
               r"\\[var]?[Tt]heta":r" theta ", \
               r"\\iota":r" iota ", \
               r"\\[var]?kappa":r" kappa ", \
               r"\\[Ll]ambda":r" lambda ", \
               r"\\mu":" mu ", \
               r"\\nu":" nu ", \
               r"\\[Xx]i ":r" xi ", \
               r"\\[var]?[Pp]i":" pi ", \
               r"\\[var]?rho ":r" rho ", \
               r"\\[var]?[Ss]igma ":r" sigma ", \
               r"\\tau":" tau ", \
               r"\\[Uu]psilon":" upsilon ", \
               r"\\[var]?[Pp]hi":" phi ", \
               r"\\chi":" chi ", \
               r"\\[Pp]si":" psi ", \
               }

    trig = {r"\\sin":" sine ", r"\\cos":" cosine ", \
            r"\\arcsin":" arc sine ", \
            r"\\arccos":" arc cosine ", \
            }

    othersym = {r"\\hbar":" hbar ", \
                   r"\\nabla":" nabla ", \
                   r"\\infty":" infinity ", \
                   r"\$?\\sim\$?":" around ", \
                   r"\\propto":r" proportional to ", \
                   r"\\neq":r"not equal to", \
                   r"\\equiv":" equivalent to ", \
                   r"\\approx":" approximately ", \
                   r" ?\> ?":" greater than ", \
                   r" ?\< ?":" less than ", \
                   r"\\times":r" times ", \
                   r"\\pm":r" plus minus", \
                   r"\\mp":r" minus plus", \
                   }

    font_formats = {r"\\rm ?":r"", \
                    r"\\mathrm ?":r"", \
                    r"\\textbf{(.*)}":r" \g<1> ", \
                    r"\\textit{(.*)}":r" \g<1> ", \
                    r"\\emph{(.*)}":r" \g<1> ", \
                    r"\\small ?":r"", \
                    }
    
    groups ={r"([A-Za-z]+)\-\-([A-Za-z]+)":r" \g<1>-\g<2>", \
            r"(\d+) ?\-\- ?(\d+)":r"\g<1> to \g<2>", \
            r"([0-9]+)\.([0-9]+)":r" \g<1> point \g<2>", \
            r"\\dot{(M)}":r" \g<1> dot ", \
            r"\\textrm{(\w*)}":"\g<1>", \
            r"(\d)+\^(\d)":r"\g<1> to the power of \g<2>", \
            r"\$?(\w+)_{(.+?)}\$?":r"\g<1> sub \g<2>", \
            r"\\footnote{(.*)}(.*\.)":r"\g<2> Note \g<1>", \
            r"\$?10 ?\^{\-(\d+)}\$":r"10 to the power of negative \g<1>", \
            r"\$?10 ?\^{(\d+)}\$?":r"10 to the power of \g<1>", \
            r"\$?10\^(\d+)\$?":r"10 to the power of \g<1> ", \
            }
            
    regexs = merge_dicts(units, BodyUnits, citations, set_space,
                        misc, trig, elements, letters, othersym, 
                        font_formats, groups) 

    return regexs