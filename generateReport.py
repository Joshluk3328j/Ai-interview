import os
import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# ----------------------------
# Load lightweight model (Phi-2)
# ----------------------------
MODEL_ID = "microsoft/phi-2"

print("Loading model... this may take a minute on first run.")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

# ----------------------------
# AI Helper function
# ----------------------------
def get_ai_summary_and_rating(conversation: str):
    """Generate a summary and candidate rating (1-10) from conversation text."""
    prompt = f"""
You are an interview evaluator. Given the following interview transcript, do 2 things:
1. Provide a concise summary of the candidate’s performance.
2. Give a rating from 1 to 10, with reasoning.

Transcript:
{conversation}

Answer in this format:
Summary: <your summary>
Rating: <score>/10
    """

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.7,
            top_p=0.9
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # crude parse
    summary, rating = "N/A", "N/A"
    if "Summary:" in response:
        parts = response.split("Summary:")[-1].strip().split("Rating:")
        summary = parts[0].strip()
        if len(parts) > 1:
            rating = parts[1].strip()

    return summary, rating

# ----------------------------
# PDF Generator
# ----------------------------
def generate_report(conversation: str, filename="interview_report.pdf"):
    summary_text, rating = get_ai_summary_and_rating(conversation)

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Interview Report")
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Summary:")
    y -= 20
    c.setFont("Helvetica", 11)
    for line in textwrap.wrap(summary_text, 100):
        c.drawString(50, y, line)
        y -= 15

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Candidate Rating: {rating}")
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Transcript:")
    y -= 20
    c.setFont("Helvetica", 11)
    for line in textwrap.wrap(conversation, 100):
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)
        c.drawString(50, y, line)
        y -= 15

    c.save()
    print(f"✅ Report saved as {filename}")


# ----------------------------
# Simulated Test Conversation
# ----------------------------
if __name__ == "__main__":
    conversation = """
Interviewer: Can you tell me about yourself?
Candidate: I am a software engineer with 3 years of experience in Python and backend systems.
Interviewer: What are your strengths?
Candidate: I am good at debugging, problem solving, and collaborating in a team environment.
Interviewer: What about your weaknesses?
Candidate: Sometimes I take too much time perfecting details, but I am learning to balance speed and quality.
Interviewer: Why should we hire you?
Candidate: Because I bring strong technical skills, adaptability, and passion for learning new technologies.
"""
    generate_report(conversation)
