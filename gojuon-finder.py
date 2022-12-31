import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks 
import os

r = sr.Recognizer()
dir_list = os.listdir("audio")
ExtT = False
chunkN, chunkNE, chunkNS = [0,0], [0,0], [0,-15]


for i in dir_list:
    ExtT = False
    file = f"audio/{i}"
    iExt = os.path.splitext(i)
    if iExt[1] == ".mp3":
        sound = AudioSegment.from_mp3(file)
        sound.export(f"audio/{iExt[0]}.wav", format="wav")
        file = f"audio/{iExt[0]}.wav"
        ExtT = True
    elif iExt[1] == ".mp4":
        sound = AudioSegment.from_file(file, "mp4")
        sound.export(f"audio/{iExt[0]}.wav", format="wav")
        file = f"audio/{iExt[0]}.wav"
        ExtT = True
    elif iExt[1] == ".wav":
        ExtT = True
    elif os.path.basename(i) != "chunks":
        print(f"[{i}] not supported file type")

    if ExtT == True:
        audioA = AudioSegment.from_file(file)
        for audioC in make_chunks(audioA, 15000):
            chunkN[1] += 15
            if chunkN[1] == 60:
                chunkN[1] = 0
                chunkN[0] += 1
            chunkNS[1] += 15
            if chunkNS[1] == 60:
                chunkNS[1] = 0
                chunkNS[0] += 1
            if audioA.duration_seconds < ((chunkN[0]*60)+chunkN[1]):
                chunkNE = divmod(audioA.duration_seconds, 60)
            else:
                chunkNE = (divmod((chunkN[0]*60)+chunkN[1], 60))
            chunkT = f"{chunkNS[0]}:{chunkNS[1]} - {int(chunkNE[0])}:{int(chunkNE[1])}"

            if os.path.exists("audio/chunks/chunk1.wav"):
                os.remove("audio/chunks/chunk1.wav")
            audioC.export("audio/chunks/chunk1.wav", format="wav")
            audioF = sr.AudioFile("audio/chunks/chunk1.wav")
            with audioF as source:
                r.adjust_for_ambient_noise(source)
                audioR = r.record(source)
                type(audioR)
                try:
                    with open("outputs.txt","a", encoding="utf-8") as f:
                        f.write("".join((f"[{i}] {chunkT} : \n", repr(r.recognize_google(audioR, language="zh-TW")), "\n\n")))
                except sr.UnknownValueError:
                    print(f"can not recognize audio from file: [{i}] in {chunkT}")
    chunkN, chunkNE, chunkNS = [0,0], [0,0], [0,-15]
    ExtT = False