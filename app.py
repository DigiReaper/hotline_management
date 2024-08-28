from flask import Flask, render_template, send_file, abort
import os
from report_generator import generate_report_from_transcript

app = Flask(__name__)

# Path to the output directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

@app.route("/")
def index():
    # List all conversations
    conversations = os.listdir(OUTPUT_DIR)
    return render_template("index.html", conversations=conversations)

@app.route("/conversation/<conversation_id>")
def conversation(conversation_id):
    conversation_path = os.path.join(OUTPUT_DIR, conversation_id)
    
    print(conversation_path)

    if not os.path.exists(conversation_path):
        abort(404)

    # Read the transcript
    transcript_file = os.path.join(conversation_path, "transcript.txt")
    with open(transcript_file, "r", encoding="utf-8") as f:
        transcript = f.read()

    # Path to the report
    report_file = os.path.join(conversation_path, f"report_{conversation_id}.pdf")

    # Trigger report generation if not found
    # if not os.path.exists(report_file):
    #     # abort(404)
    #     report_file = generate_report_from_transcript(transcript_file, conversation_id, conversation_path)

    return render_template("conversation.html", conversation_id=conversation_id, transcript=transcript, report_file=report_file)

@app.route("/download/<conversation_id>")
def download_report(conversation_id):
    conversation_path = os.path.join(OUTPUT_DIR, conversation_id)
    report_file = os.path.join(conversation_path, f"report_{conversation_id}.pdf")

    # if not os.path.exists(report_file):
    #     abort(404)
    
    if not os.path.exists(report_file):
    # abort(404)
        transcript_file = os.path.join(conversation_path, "transcript.txt")
        report_file = generate_report_from_transcript(transcript_file, conversation_id, conversation_path)

    return send_file(report_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)