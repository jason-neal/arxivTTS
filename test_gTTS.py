# test_gTTS.py

from gtts import gTTS


Text = "This should be saved as a mp3. This should be saved as a mp3. This should be saved as a mp3"
print("Length", len(Text))

tts = gTTS(text="Text", lang="en") 
tts.save("hello.mp3")

#.HTTP Error 503: Service Unavailable
import GoogleTTS
# GoogleTTS.audio_extract(input_text='tunnel snakes rule apparently', args = {'language':'en','output':'outputto.mp3'})