import pyttsx

print(pyttsx.init("espeak"))

engine = pyttsx.init()
engine.say('Sally sells seashells by the seashore.')
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()

# import pyttsx
def onStart(name):
   print 'starting', name
def onWord(name, location, length):
   print 'word', name, location, length
def onEnd(name, completed):
   print 'finishing', name, completed
engine = pyttsx.init()
engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()

#import pyttsx
def onWord(name, location, length):
   print 'word', name, location, length
   if location > 10:
      engine.stop()
engine = pyttsx.init()
engine.connect('started-word', onWord)
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()

# engine = pyttsx.init()
# voices = engine.getProperty('voices')
# print(voices)
# for voice in voices:
#    engine.setProperty('voice', voice.id)
#    engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()


