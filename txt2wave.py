#txt2wave.py

import subprocess
#import subprocess
# To convert the txt file to wave
fname = "micinpainting_rvt.txt"
outname = "test_subprocess.wav"
subprocess.call(["text2wave " + fname + " -o " + outname], shell=True)




# 
