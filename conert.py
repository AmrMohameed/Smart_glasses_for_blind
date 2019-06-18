from pydub import AudioSegment
sound = AudioSegment.from_mp3("voice.mp3")
sound.export("voice.wav", format="wav")