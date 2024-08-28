import argparse
import os
import threading
import time
import tkinter as tk
from tkinter import scrolledtext
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

def start_conversation(language):
    global stop_signal
    stop_signal = False
    stop_thread = threading.Thread(target=monitor_stop_signal)
    stop_thread.start()
    main(language)
    stop_thread.join()

def on_start_button_click(language):
    threading.Thread(target=start_conversation, args=(language,)).start()

def create_gui():
    root = tk.Tk()
    root.title("Cybercrime Bot")

    # Language Selection
    language_label = tk.Label(root, text="Select Language:")
    language_label.pack()

    language_var = tk.StringVar(value='en')
    languages = [("English", 'en'), ("Telugu", 'te'), ("Hindi", 'hi')]
    for text, lang in languages:
        tk.Radiobutton(root, text=text, variable=language_var, value=lang).pack()

    # Start Button
    start_button = tk.Button(root, text="Start Conversation", command=lambda: on_start_button_click(language_var.get()))
    start_button.pack()

    # Stop Button
    stop_button = tk.Button(root, text="Stop Conversation", command=lambda: setattr(globals(), 'stop_signal', True))
    stop_button.pack()

    # Conversation Log
    log_label = tk.Label(root, text="Conversation Log:")
    log_label.pack()

    log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
    log_text.pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()