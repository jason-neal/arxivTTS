ArxivTTS 
========
The goal of this script is to turn arxiv articles into audio with text-to-speech (TTS) to be listened to.

It downloads the source for the article and then parses the tex file to extract the main article text.

Currently the text is sent to an external TTS program text2wav to save the spoken article as a wav file.

##Requirements/Dependencies

#####Python modules
These may need to be ran with sudo.
	* [argparse](https://docs.python.org/2/howto/argparse.html)
	* [re](https://docs.python.org/2.7/library/re.html)	
	* [requests](http://docs.python-requests.org/en/latest/)
	* [tarfile](https://docs.python.org/2/library/tarfile.html)
	* [Arxiv.py](http://stringwiki.org/wiki/ArXiv_script) 

`pip install argparse`
`pip install re`
`pip install requests`
`pip install tarfile`

 Arxiv.py needs tobe downloaded manually from the wiki.
#####TTS
	festival (text2wav specifically)

####Other TTS engines
There are a number of other TTS options available.

These still need some testing to find the best TTS engine and good voices.

These are

####Python modules 
pyttsx  - platform independant
	pip install pyttsx

gtts?
	pip install gtts

GoogleTTS

####Linux programs
	espeak - used with pyttsx
	festival - text2wave


##Running 

It can be run from the command line like

	python arxivTTS.py {arxiv reference}

or 

	arxivTTS.py {arxiv reference}

if made executable with `chmod +x arxivTTS.py`.

Arxiv References
----------------
The arxiv reference can be any of the urls to the article aswell as just the artilce number

e.g. These should all be valid {arxiv reference} to find the same article.
```
1512.03000
http://arxiv.org/abs/1512.03000
http://arxiv.org/pdf/1512.03000v1.pdf
http://arxiv.org/format/1512.03000v1
http://arxiv.org/e-print/1512.03000v1
```

If there is no source code available for the article then arxivTTS will not work and crash.

Options
-------
	-o 	output file name
	-k  keep the downloaded source file
	-t  Audio file type to export as

#####Future options
autoplay
choose voice

playback speed

TTS engine to use

Contributions
-------------
Please feel free to make issues or comments and suggestions for improvements.
Please send any references of articles that are not filtered correctly so that I can improve the latex filtering.


