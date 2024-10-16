import os
import yt_dlp
import whisper

# Step 1: Download YouTube Video Audio
def download_audio_from_youtube(video_url, output_dir="audio_files"):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set yt-dlp options for audio extraction
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Download the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Get the downloaded audio file path
    info_dict = ydl.extract_info(video_url, download=False)
    title = info_dict.get('title', None)
    audio_file_path = os.path.join(output_dir, f"{title}.mp3")

    return audio_file_path, title

# Step 2: Transcribe Audio to Text using Whisper
def transcribe_audio_to_text(audio_file_path, model_type="base"):
    # Load the Whisper model
    model = whisper.load_model(model_type)

    # Transcribe the audio file
    result = model.transcribe(audio_file_path)

    # Get the transcribed text
    return result['text']

# Step 3: Save Transcription to Text File in Result Folder
def save_transcription_to_file(text, title, result_dir="result"):
    # Create result directory if it doesn't exist
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # Save the transcription text to a .txt file in the result directory
    file_path = os.path.join(result_dir, f"{title}.txt")
    with open(file_path, "w") as f:
        f.write(text)

    return file_path

# Main Function
if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")

    print("Downloading audio from YouTube...")
    audio_file_path, title = download_audio_from_youtube(video_url)
    print(f"Audio downloaded at: {audio_file_path}")

    print("Transcribing audio to text...")
    transcription = transcribe_audio_to_text(audio_file_path)
    print("Transcription complete.")

    # Save transcription to the result folder
    transcription_file = save_transcription_to_file(transcription, title)
    print(f"Transcription saved to: {transcription_file}")
