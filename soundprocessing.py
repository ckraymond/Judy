import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI

# import wavio as wv

# Sampling frequency
freq = 44100

# Recording duration
duration = 5

# Start recorder with the given values of
# duration and sample frequency
recording = sd.rec(int(duration * freq),
                   samplerate=freq, channels=1)

# Record audio for the given number of seconds
sd.wait()

write("../Desktop/test_recording.wav", freq, recording)

client = OpenAI()

audio_file= open("../Desktop/test_recording.wav", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file
)
print(transcription.text)

