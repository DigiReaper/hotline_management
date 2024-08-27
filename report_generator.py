import openai
from fpdf import FPDF
import os

from config import OPENAI_API_KEY, SYSTEM_PROMPT
from openai import OpenAI

openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_report(conversation, conversation_id, conversation_path):
    # Define the system message for GPT-3.5 Turbo
    SYSTEM_PROMPT = {
        "role": "system",
        "content": (
            "You are an AI assistant generating a detailed report based on a conversation about a cybercrime incident. "
            "Use the following template to structure the report:\n\n"
            "Cybercrime Incident Report\n"
            "--------------------------\n"
            "Conversation ID: {conversation_id}\n\n"
            "1. **Caller Details**:\n"
            "   - Name: [Caller Name]\n"
            "   - Contact Number: [Contact Number]\n"
            "   - Email: [Email Address]\n"
            "   - Identification Details: [Identification Details]\n\n"
            "2. **Incident Details**:\n"
            "   - Date & Time: [Incident Date and Time]\n"
            "   - Nature of the Cybercrime: [Cybercrime Type]\n"
            "   - Description: [Detailed Description of the Incident]\n\n"
            "3. **Accused Details**:\n"
            "   - Name: [Accused Name]\n"
            "   - Contact Information: [Accused Contact Information]\n"
            "   - Relationship to Caller: [Relationship]\n\n"
            "4. **Platform Information**:\n"
            "   - Platform/Service: [Platform Name]\n"
            "   - Account Details: [Account Details]\n\n"
            "5. **Evidence Provided**:\n"
            "   - [Evidence Details]\n\n"
            "Generate the report based on the details provided in the conversation below."
        )
    }

    # Provide the conversation to GPT-3.5 Turbo
    messages = [SYSTEM_PROMPT] + [{"role": entry['role'], "content": entry['content']} for entry in conversation]

    response = openai_client.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1500
    )

    report_content = response['choices'][0]['message']['content']

    # Save the report as a PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, report_content)
    
    pdf_output = os.path.join(conversation_path, f"report_{conversation_id}.pdf")
    pdf.output(pdf_output)
    
    return pdf_output


def generate_report_from_transcript(transcript_path, conversation_id, output_dir):
    # Read the transcript from the text file
    with open(transcript_path, "r") as file:
        transcript = file.read()

    # Define the system prompt template for generating the report
    system_prompt_template = """
    You are an AI designed to help generate formal incident reports from conversation transcripts. Below is a conversation transcript regarding a cybercrime incident. Please create a detailed and structured report that includes:

    1. **Incident Overview**: Summarize the incident.
    2. **Victim Information**: Include name, contact details, and any other identification provided.
    3. **Incident Details**: Include the date, time, and description of the incident.
    4. **Accused Information**: Include any details about the accused (if provided).
    5. **Supporting Evidence**: Mention any evidence the victim has shared or plans to share.
    6. **Next Steps**: Outline what will happen next or any advice given to the victim.

    Conversation Transcript:
    {transcript}
    """

    # Format the prompt
    system_prompt = system_prompt_template.format(transcript=transcript)

    # Request GPT-3.5 Turbo to generate the report
    response = openai_client.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt}
        ]
    )

    # Extract the generated report from the response
    report_text = response['choices'][0]['message']['content']

    # Define the output PDF path
    report_pdf_path = os.path.join(output_dir, f"report_{conversation_id}.pdf")

    # Create the PDF report
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, report_text)

    # Save the PDF report
    pdf.output(report_pdf_path)

    return report_pdf_path

# Example usage:
# conversation_id = "sample_id_123"
# transcript_path = f"output/{conversation_id}/transcript.txt"
# output_dir = f"output/{conversation_id}"
# generate_report_from_transcript(transcript_path, conversation_id, output_dir)
