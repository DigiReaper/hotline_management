from azure.cognitiveservices.speech import AudioConfig, SpeechSynthesizer
from config import speech_config

def speak_text(text, language='en'):
    print(f"Speaking: {text}")
    if language == 'te':
        speech_config.speech_synthesis_voice_name = "te-IN-ShrutiNeural"
    elif language == 'hi':
        speech_config.speech_synthesis_voice_name = "hi-IN-MadhurNeural"
    else:
        speech_config.speech_synthesis_voice_name = "en-IN-AaravNeural"

    audio_config = AudioConfig(device_name="default")
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason == result.reason.Canceled:
        print(f"Speech synthesis canceled: {result.cancellation_details.reason}")
        print(f"Error details: {result.cancellation_details.error_details}")
