import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio_from_video(video_path):
    """
    Extracts audio from a video and transcribes it to text using SpeechRecognition.
    """
    audio_path = "temp_audio.wav"

    # Extract audio
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, codec="pcm_s16le")
    print(f"Audio extracted to {audio_path}")

    # Transcribe audio
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(audio_path)

    # Split audio into chunks for better accuracy
    chunk_length_ms = 60000  # 60 seconds per chunk
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    full_text = ""
    for i, chunk in enumerate(chunks):
        chunk.export(f"chunk_{i}.wav", format="wav")
        with sr.AudioFile(f"chunk_{i}.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                full_text += text + " "
                print(f"Chunk {i} transcribed successfully.")
            except sr.UnknownValueError:
                print(f"Chunk {i}: Speech unclear.")
            except sr.RequestError as e:
                print(f"Chunk {i}: API error - {e}")

    # Cleanup
    os.remove(audio_path)
    for i in range(len(chunks)):
        os.remove(f"chunk_{i}.wav")

    return full_text

def main():
    video_path = "/Users/kritsadakruapat/Desktop/Collage/CSX4202(541)Datamining/prep-mid/p4.mov"  # Replace with your video file

    # Transcribe audio from video
    print("Transcribing audio...")
    audio_transcription = transcribe_audio_from_video(video_path)

    # Save audio transcription
    output_folder = "p4"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    audio_text_file = os.path.join(output_folder, "audio_text.txt")
    with open(audio_text_file, "w", encoding="utf-8") as file:
        file.write(audio_transcription)

    print(f"Audio transcription complete. Results saved in {audio_text_file}")

if __name__ == "__main__":
    main()
