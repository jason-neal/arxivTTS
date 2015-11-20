""" Attempt article to wave by filtering  html instead of text file"""
"""html will be much more difficult so going back to just text"""

import subprocess

def extract_html(filename):
	""" Run command line code pdftohtml"""
	"""  pdftohtml [options] <PDF-file> [<HTML-file> <XML-file>]
	-s output as single page, -i ignore images
    """
    #infile = filename + '.pdf'
    #testreplace = infile
    outputfile = filename.replace('.pdf','.html')
	subprocess.call(['pdftohtml','-s','-i', filename, outputfile])
	return outputfile


def save_filtered_text(filename):
    outfile =filename.replace('.pdf','.txt')
    pass


def create_audio(filename, ext='.mp3'):
	""" Run the command tool txt2wave """
	outfile =filename.replace('.pdf',ext)
	outfile =outfile.replace('.html',ext)
    outfile =outfile.replace('.txt',ext)
	subprocess.call()
	pass