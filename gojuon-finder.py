# imports
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks 
import os

# class and vars
r = sr.Recognizer()
ExtT = False
chunkN, chunkNE, chunkNS = [0,0], [0,0], [0,-15]

# main process
for i in os.listdir("audio"): # loop through the audio file
    ExtT = False
    if not os.path.exists("audio/conversion"):
        os.mkdir("audio/conversion")
    file = f"audio/{i}" 
    # check file extention
    iExt = os.path.splitext(i)
    if iExt[1] == ".mp3":
        AudioSegment.from_mp3(file).export(f"audio/conversion/{iExt[0]}.wav", format="wav")
        file = f"audio/{iExt[0]}.wav" # export a new converted version of audio to audio/conversion/
        ExtT = True
    elif iExt[1] == ".mp4":
        AudioSegment.from_file(file, "mp4").export(f"audio/conversion/{iExt[0]}.wav", format="wav")
        file = f"audio/{iExt[0]}.wav" # export a new converted version of audio to audio/conversion/
        ExtT = True
    elif iExt[1] == ".wav":
        AudioSegment.from_file(file).export(f"audio/conversion/{iExt[0]}.wav", format="wav")
        ExtT = True # export a new converted version of audio to audio/conversion/
    elif os.path.basename(i) != "chunks" and os.path.basename(i) != "conversion":
        print(f"[{i}] not supported file type") # skip that wrong extension file

    # start speech recognition if file extension is right
    if ExtT == True: 
        audioA = AudioSegment.from_file(file)
        for audioC in make_chunks(audioA, 15000): # make audio into chunks
            chunkN[1] += 15 # keep track of the Nth chunk (time)
            if chunkN[1] == 60:
                chunkN[1] = 0
                chunkN[0] += 1
            chunkNS[1] += 15 # Nth chunk start
            if chunkNS[1] == 60:
                chunkNS[1] = 0
                chunkNS[0] += 1
            if audioA.duration_seconds < ((chunkN[0]*60)+chunkN[1]): # Nth chunk end
                chunkNE = divmod(audioA.duration_seconds, 60)
            else:
                chunkNE = (divmod((chunkN[0]*60)+chunkN[1], 60))
            chunkT = f"{chunkNS[0]}:{chunkNS[1]} - {int(chunkNE[0])}:{int(chunkNE[1])}"

            # export the chunk audio to audio/chunks/
            if os.path.exists("audio/chunks/chunk1.wav"):
                os.remove("audio/chunks/chunk1.wav")
            if not os.path.exists("audio/chunks"):
                os.mkdir("audio/chunks")
            audioC.export("audio/chunks/chunk1.wav", format="wav")
            audioF = sr.AudioFile("audio/chunks/chunk1.wav")
            # start speech recognition and output the results to output.txt
            with audioF as source:
                audioR = r.record(source)
                type(audioR)
                try:
                    with open("outputs.txt","a", encoding="utf-8") as f:
                        f.write("".join((f"[{i}] {chunkT} : \n", repr(r.recognize_google(audioR, language="zh-TW(cmn-Hant-TW)")), "\n\n")))
                except sr.UnknownValueError:
                    with open("outputs.txt","a", encoding="utf-8") as f:
                        f.write(f"cannot recognize audio from file: [{i}] in {chunkT}")

    # reset vars
    chunkN, chunkNE, chunkNS = [0,0], [0,0], [0,-15]
    ExtT = False

# delete used files and folders after the process
for uneededfile in os.listdir("audio/conversion"):    
    os.remove(f"audio/conversion/{uneededfile}")
os.remove(f"audio/chunks/chunk1.wav")
os.rmdir("audio/chunks")
os.rmdir("audio/conversion")