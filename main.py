import argparse
import os
import threading
import time
from conversation_manager import generate_response, create_conversation_directory
from speech_recognition import record_audio, transcribe_audio
from text_to_speech import speak_text
from report_generator import generate_report
import keyboard

# Global Variables
stop_signal = False

def monitor_stop_signal():
    global stop_signal
    while not stop_signal:
        if keyboard.is_pressed('F3'):
            print("F3 pressed. Stopping the application...")
            stop_signal = True
            #break
        time.sleep(0.1)
        
def main(language):
    history = []
    global stop_signal

    conversation_id, conversation_path = create_conversation_directory()

    while not stop_signal:
        if stop_signal:
            break
        
        # Record and Transcribe
        if language == 'en':
            audio_file = record_audio()
        user_text = transcribe_audio(language)
        history.append({'role': 'user', 'content': user_text})

        # Save the transcript
        with open(os.path.join(conversation_path, "transcript.txt"), "a", encoding="utf-8") as f:
            f.write(f"User: {user_text}\n")

        # Generate Response
        assistant_text = generate_response(history)
        history.append({'role': 'assistant', 'content': assistant_text})

        # Save the transcript
        with open(os.path.join(conversation_path, "transcript.txt"), "a" , encoding="utf-8") as f:
            f.write(f"Assistant: {assistant_text}\n")
            
        if stop_signal:
            break

        # Text-to-Speech
        speak_text(assistant_text, language)

        # Check if conversation should end
        if 'end conversation' in user_text.lower():
            break

    # Generate Report
    report_path = generate_report(history, conversation_id, conversation_path)
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cybercrime Bot")
    parser.add_argument('-te', '--telugu', action='store_true', help="Use Telugu language")
    parser.add_argument('-en', '--english', action='store_true', help="Use English language (default)")
    parser.add_argument('-hi', '--hindi', action='store_true', help="Use Hindi language")

    args = parser.parse_args()
    
    stop_thread = threading.Thread(target=monitor_stop_signal)
    stop_thread.start()

    if args.telugu:
        main('te')
    elif args.hindi:
        main('hi')
    else:
        main('en')
        
    stop_thread.join()

    
