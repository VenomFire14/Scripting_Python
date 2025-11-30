import pyaudio
import wave
import time
import whisper
import os

# ---------------- SETTINGS ----------------
SAVE_FOLDER = "meeting_records"
AUDIO_FILENAME = "meeting_audio.wav"
TEXT_FILENAME = "meeting_transcript.txt"
RECORD_SECONDS = 10   # Change recording duration (in seconds)
# ------------------------------------------


# Create folder if not exists
os.makedirs(SAVE_FOLDER, exist_ok=True)


def record_audio(path):
    """Records audio from microphone and saves it to a WAV file."""
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 16000  # Whisper works best at 16k sample rate

    print("\n🎤 Recording started... Speak now!")
    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    for _ in range(0, int(fs / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save audio
    wf = wave.open(path, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b"".join(frames))
    wf.close()

    print(f"📁 Audio saved at: {path}")


def transcribe_audio(audio_path, text_path):
    """Transcribes audio using Whisper and saves the text."""
    print("\n🔍 Transcribing audio, please wait...")

    model = whisper.load_model("base")   # Options: tiny, base, small, medium, large
    result = model.transcribe(audio_path)

    text = result["text"]

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"📝 Transcript saved at: {text_path}")
    print("\nFinal Transcript:\n")
    print(text)


if __name__ == "__main__":
    audio_path = os.path.join(SAVE_FOLDER, AUDIO_FILENAME)
    text_path = os.path.join(SAVE_FOLDER, TEXT_FILENAME)

    record_audio(audio_path)
    transcribe_audio(audio_path, text_path)
