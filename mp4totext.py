from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment

def mp4_to_text(mp4_file):
    # Step 1: Convert MP4 to Audio
    video = VideoFileClip(mp4_file)
    audio_path = "audio.wav"
    video.audio.write_audiofile(audio_path, codec="pcm_s16le")

    # Step 2: Transcribe Audio to Text
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(audio_path)

    # Split audio for better accuracy if needed
    audio_chunks = audio[::60000]  # 60 seconds each chunk
    full_text = ""

    for i, chunk in enumerate(audio_chunks):
        chunk.export("chunk.wav", format="wav")
        with sr.AudioFile("chunk.wav") as source:
            audio_data = recognizer.record(source)
            try:
                # Recognize speech using Google Web Speech API (free, but limited usage)
                text = recognizer.recognize_google(audio_data)
                full_text += text + " "
            except sr.UnknownValueError:
                print("Audio not clear")
            except sr.RequestError:
                print("API unavailable")

    return full_text

# Usage example
mp4_file = "Bro.Amnual01.mp4"
text = mp4_to_text(mp4_file)
print(text)
