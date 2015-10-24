#!/bin/bash

if [ -z "$1" ]; then 
    $filename = $1
else
    echo "Enter pdf name:" 
    read filename
fi

#pdf2txt $filename > tmptext.txt
ebook-convert $filename > tmptext.txt

# add text file editing command here

festival --tts tmptext.txt

