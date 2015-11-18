#!/bin/bash

if [ -z "$1" ]; then 
    $filename = $1
else
    echo "Enter pdf name:" 
    read filename
fi

pdf2txt $filename > tmptext.txt
#ebook-convert $filename > tmptext.txt

# add text file editing command here
python articlefilter.py tmptext.txt filtered_txt/filtered.txt
#festival --tts tmptext.txt
text2wave /filtered_txt/filtered.txt -o output/filtered_wave.mp3
