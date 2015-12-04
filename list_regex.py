
""" Processing tex commands to words using regular expresions.

Edit these lists to include extra expressions as they are incountered """
import re

def cat_lists(*list_args):
    """
    Given any number of lists, concatinate onto a new list
    """
    result = []
    for List in list_args:
        result.extend(List)

    return result

def regex_sub(data):
    """ Subsitute latex for words"""
    regexs = regex_lists()
    
    for pair in regexs:
        pattern = pair[0]
        replacement = pair[1]     
        data = re.sub(pattern, replacement, data)
       
    # Junk to make still present issues stand out in txt file 
    #data = re.sub(r"\\(.*?){", "#### REVEALING \g<1> REVEALING ####", data)
    return data

def regex_lists(): 
    """ Regex for replacement"""
      
    space = [(r"\\\,", " "), \
                 (r"\~", " "), \
                 ]
   
    font_formats = [(r"\\rm ?", r""), \
                    (r"\\mathrm ?", r""), \
                    (r"\\textbf{(.*?)}", r" \g<1> "), \
                    (r"\\textit{(.*?)}", r" \g<1> "), \
                    (r"\\emph{(.*?)}", r" \g<1> "), \
                    (r"\\small ?", r""), \
                    ]    
    elements = [(r"\$\^{60}\$Fe", " Iron-60"), \
                (r"\$\^{26}\$Al", "Aluminium-26"), \
                ]

    powers = [(r"m( |\\,)?s\$\^{-1}\$", r" meters per second "), \
              (r"( |\\,)s\$\^{-1}\$", r" per second "), \
              (r"( |\\,)s\$\^{-2}\$", r" per second squared "), \
              (r" ([A-Za-z]+ ?)\$?\^{-2}\$?", r" per \g<1> squared "), \
              (r" ?\^\{2\}\$?", r" squared"), \
              (r" ?\^\{3\}\$?", r" cubed"), \
              (r"\$?(\d+) ?\^{?\-(\d+)}?\$?", r"\g<1> to the power of negative \g<2>"), \
              (r"\$?(\d+) ?\^{?(\d+)}?\$?", r" \g<1> to the power of \g<2> "), \
              (r"\$\^{?(\d+)}?\$", r" to the power of \g<1> "), \
              ]        

    symbols = [(r"\\hbar", " hbar "), \
                (r"\\nabla", " nabla "), \
                (r"\\infty", " infinity "), \
                (r"\$?\\sim\$?", " is of order of "), \
                (r"\\propto", r" proportional to "), \
                (r"\\neq", r" not equal to "), \
                (r"\\geq", r" greater than or equal to "), \
                (r"\\leq", r" less than or equal to "), \
                (r"\\equiv", r" equivalent to "), \
                (r"\\approx", r" approximately "), \
                (r"\\simeq", r" approximately equal to "), \
                (r" ?\> ?", r" greater than "), \
                (r" ?\< ?", r" less than "), \
                (r"\\times", r" times "), \
                (r"\\pm", r" plus minus "), \
                (r"\\mp", r" minus plus "), \
                (r"\\%", r" percent "), \
                (r"\\dot{(\w*)}", r" \g<1> dot "), \
                ]

    trig = [(r"\\sin", " sine ", r"\\cos", " cosine "), \
            (r"\\arcsin", " arc sine "), \
            (r"\\arccos", " arc cosine "), \
            ]

    greek = [(r"\\aplha", r" aplha "), \
             (r"\\[b]eta", r" beta "), \
             (r"\\[Gg]amma", r" gamma "), \
             (r"\\[Dd]elta", r" delta "), \
             (r"\\[var]?epsilon", r" epsilon "), \
             (r"\\zeta", r" zeta "), \
             (r"\\eta", r" eta "), \
             (r"\\[var]?[Tt]heta", r" theta "), \
             (r"\\iota", r" iota "), \
             (r"\\[var]?kappa", r" kappa "), \
             (r"\\[Ll]ambda", r" lambda "), \
             (r"\\mu", r" mu "), \
             (r"\\nu", r" nu "), \
             (r"\\[Xx]i", r" xi "), \
             (r"\\[var]?[Pp]i", r" pi "), \
             (r"\\[var]?rho", r" rho "), \
             (r"\\[var]?[Ss]igma", r" sigma "), \
             (r"\\tau", r" tau "), \
             (r"\\[Uu]psilon", r" upsilon "), \
             (r"\\[var]?[Pp]hi", r" phi "), \
             (r"\\chi", r" chi "), \
             (r"\\[Pp]si", r" psi "), \
             ]

    solarsys = [(r"M ?\$?\_{?\\oplus}?\$?", r" Earth masses "), \
               (r"M ?\$?\_{?\\odot}?\$?", r" Solar masses "), \
               (r"M ?\$?\_{?\\star}?\$?", r" Stellar masses "), \
               (r"R ?\$?\_{?\\oplus}?\$?", r" Earth radii "), \
               (r"R ?\$?\_{?\\odot}?\$?", r" Solar radii "), \
               (r"R ?\$?\_{?\\star}?\$?", r" Stellar radii "), \
               (r"\$?M\$?\_{Jup}\$?", r" Jupiter masses "), \
               (r"R\$?\_{Jup}\$?", r" Jupiter radii "), \
               (r"AU", r"AU"), \
               (r"[^MR]\_\\oplus", r" Earth "), \
               (r"[^MR]\_\\odot", r" Sun "), \
               (r"[^MR]\_\\star", r" Star "), \
               ]

    units = [(r"( .*[^A-Za-z])pc[^A-Za-z]", r"\g<1> parsec "), \
            (r"[^A-Za-z]\\?mu ?m[^A-Za-z] ?", r" micrometers "), \
            (r"( .*[^A-Za-z])km[^A-Za-z]", r" kilometers "), \
            (r"( .*[^A-Za-z])nm[^A-Za-z]", r"\g<1> nanometers "), \
            (r"( |\\,)cm[^A-Za-z]", r"\g<1> centimeters "), \
            (r"(\d+)( |\\,)m[^A-Za-z]", r"\g<1> meters "), \
            (r"( .*[^A-Za-z])Hz[^A-Za-z]", r"\g<1> Hertz "), \
            (r" ?\\AA ?", r" Angstroms "), \
            (r" ?Myr ?", r" Mega years "), \
            (r'(\d+)\"(.?\,? )', r"\g<1> arcsecond\g<2>"), \
            ]  # [^A-Za-z] not another letter before or after (i.e. can't match in a word)
         
    abrev = [(r" ?SNR ?", r" signal to noise ratio "), \
             (r" ?S/N ?", r" Signal to noise "), \
             (r" ?Fig\. ?", r" Figure "), \
             (r" ?Eq\. ?", r" Equation "), \
             ] 

    other = [(r"([A-Za-z]+)\-\-([A-Za-z]+)", r" \g<1>-\g<2>"), \
             (r"(\d+) ?\-\- ?(\d+)", r"\g<1> to \g<2>"), \
             (r"\$?(\w+)_{(.+?)}\$?", r"\g<1> sub \g<2>"), \
             (r"(\d{1,3}) (\d{3})", r"\g<1>,\g<2>"), \
             ] 
            # (r"([0-9]+)\.([0-9]+)", r" \g<1> point \g<2>"), \
    
   
    # citations 
    # still have some issues with losing end brackets
    citations = [(r"\\cite\*?{(.*?)}{1}", r" \g<1> "), \
                 (r"\\citet\*?{(.*?)}{1}", r" \g<1> "), \
                 (r"\\citep\*?\{(.*?)}{1}", r" "), \
                 (r"\\cite[p]\*?\[(.*?)\]\[(.*)\]{(.*?)}?.?", r" "), \
                 (r"\\ref{(.*)}", " \g<1> "), \
                 (r"\\footnote{(.*)}(.*\.)", r"\g<2> Note \g<1>"), \
                 ]

    clean = [(r"\$(.*?)\$", r" \g<1> "), \
            (r" +", r" "), \
            (r"{", r""), \
            (r"}", r""), \
            ]
    accents = []
    

    # Need to be careful of ordering
    regexs = cat_lists(space, font_formats, elements, powers, symbols, trig, greek, 
                        solarsys, units, abrev, other, citations, 
                        accents, clean)
   
    return regexs