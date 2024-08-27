import wave
import pyaudio
from config import MODEL_SIZE, DEVICE, AZURE_SPEECH_KEY, AZURE_SERVICE_REGION
import azure.cognitiveservices.speech as speechsdk
from faster_whisper import WhisperModel
import keyboard
# from main import stop_signal

def record_audio():
    # if stop_signal:
    #     return "voice_record.wav"
    
    audio = pyaudio.PyAudio()
    frames = []

    print("Recording... Press 'space' to stop.")
    py_stream = audio.open(rate=16000, format=pyaudio.paInt16, channels=1, input=True, frames_per_buffer=512)

    while not keyboard.is_pressed('space'):
        frames.append(py_stream.read(512))
        # if stop_signal:
        #     break

    py_stream.stop_stream()
    py_stream.close()
    audio.terminate()

    with wave.open("voice_record.wav", 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))

    return "voice_record.wav"

def transcribe_audio(language='en'):
    if language == 'en':
        model = WhisperModel(model_size_or_path=MODEL_SIZE, device=DEVICE)
        transcription = " ".join(seg.text for seg in model.transcribe("voice_record.wav", language="en")[0])
    else:
        l = language + "-IN"
        # print(f"Transcribing in {l}...")
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SERVICE_REGION, speech_recognition_language=l)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
        print("Listening...")
        result = speech_recognizer.recognize_once()
        
        

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            transcription = result.text
        else:
            transcription = ""

    print(f"Transcription: {transcription}")
    return transcription
