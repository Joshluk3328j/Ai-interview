import sys
import json
import re
import torch
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ---------------------------------------
# Model selection with graceful fallback
# ---------------------------------------
CANDIDATE_MODELS = [
    "google/flan-t5-large", # good balance of quality & size
    "google/flan-t5-base"   # lighter fallback
]

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def load_best_model():
    last_error = None
    for name in CANDIDATE_MODELS:
        try:
            print(f"📥 Loading model: {name} on {DEVICE} ...")
            tok = AutoTokenizer.from_pretrained(name)
            mdl = AutoModelForSeq2SeqLM.from_pretrained(name)
            mdl.to(DEVICE)
            mdl.eval()
            print("✅ Model loaded.")
            return name, tok, mdl
        except Exception as e:
            print(f"⚠️ Failed to load {name}: {e}")
            last_error = e
    raise RuntimeError(f"Could not load any model. Last error: {last_error}")

MODEL_NAME, tokenizer, model = load_best_model()

# ---------------------------------------
# Local generation helper
# ---------------------------------------
def generate(text, max_new_tokens=512):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=False
    ).to(DEVICE)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            num_beams=5,
            length_penalty=1.0,
            no_repeat_ngram_size=3,
            early_stopping=True,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# ---------------------------------------
# AI Summary & Rating
# ---------------------------------------
def get_ai_summary_and_rating(conversation):
    transcript = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation])

    prompt = f"""
You are an expert interviewer evaluating a candidate based ONLY on the transcript. 
Provide a concise evaluation with EXACTLY the following fields (one per line, same format):

Skills: <text>
Experience: <text>
Strengths: <text>
Weaknesses: <text>
Job Fit: <text>
Candidate Rating (1-10): <number>

Transcript:
{transcript}
""".strip()

    try:
        result = generate(prompt, max_new_tokens=512).strip()

        # ---- Parse sections ----
        fields = ["Skills", "Experience", "Strengths", "Weaknesses", "Job Fit"]
        sections = {}

        for field in fields:
            pattern = rf"{field}\s*:\s*(.*?)(?=\n(?:Skills|Experience|Strengths|Weaknesses|Job Fit|Candidate Rating)|\Z)"
            m = re.search(pattern, result, flags=re.DOTALL | re.IGNORECASE)
            sections[field] = m.group(1).strip() if m else "Not clearly stated."

        # ---- Parse rating ----
        rating = "N/A"
        m = re.search(r"Candidate Rating\s*:\s*(\d{1,2})", result, flags=re.IGNORECASE)
        if not m:
            m = re.search(r"(\d{1,2})\s*/\s*10", result)
        if m:
            val = int(m.group(1))
            if 1 <= val <= 10:
                rating = val
        else:
            rating = 5  # neutral default

        summary_lines = [f"{field}: {sections[field]}" for field in fields]
        summary_text = "\n".join(summary_lines)
        return summary_text, rating

    except Exception as e:
        print(f"⚠️ Error during generation: {e}")
        fallback = [
            "Skills: Not clearly stated.",
            "Experience: Not clearly stated.",
            "Strengths: Not clearly stated.",
            "Weaknesses: Not clearly stated.",
            "Job Fit: Not clearly stated.",
        ]
        return "\n".join(fallback), 5

# ---------------------------------------
# PDF Report Generator
# ---------------------------------------
def generate_report(conversation, output_file="interview_report.pdf"):
    if not conversation or not isinstance(conversation, list):
        print("⚠️ Error: Invalid or empty conversation data.")
        return

    doc = SimpleDocTemplate(output_file, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    # Title
    content.append(Paragraph("Interview Report", styles["Title"]))
    content.append(Spacer(1, 20))

    # Summary Table
    summary_text, rating = get_ai_summary_and_rating(conversation)
    table_data = [["Field", "Details"]]
    for line in summary_text.split("\n"):
        if ": " in line:
            field, details = line.split(": ", 1)
            table_data.append([field, Paragraph(details, styles["Normal"])])
    table_data.append(["Candidate Rating", f"{rating} / 10"])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))
    content.append(Paragraph("<b>Summary:</b>", styles["Heading2"]))
    content.append(table)
    content.append(Spacer(1, 20))

    # Recommendations
    content.append(Paragraph("<b>Recommendations:</b>", styles["Heading2"]))
    recommendations = (
        "Consider a follow-up interview to assess additional technical depth, "
        "team collaboration, and problem-solving under pressure."
    )
    content.append(Paragraph(recommendations, styles["Normal"]))
    content.append(Spacer(1, 20))

    # Transcript Breakdown
    content.append(Paragraph("<b>Transcript Breakdown:</b>", styles["Heading2"]))
    for msg in conversation:
        role = msg.get("role", "Unknown").capitalize()
        text = msg.get("content", "")
        content.append(Paragraph(f"<b>{role}:</b> {text}", styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)
    print(f"✅ Report saved to {output_file}")

# ---------------------------------------
# MAIN
# ---------------------------------------
if __name__ == "__main__":
    if not sys.stdin.isatty():
        raw_data = sys.stdin.read()
        conversation = json.loads(raw_data)
    else:
        conversation = [
            {"role": "interviewer", "content": "Can you tell me about yourself?"},
            {"role": "candidate", "content": "I am a software engineer with 5 years of backend development experience."},
            {"role": "interviewer", "content": "What programming languages are you most comfortable with?"},
            {"role": "candidate", "content": "I primarily work with Python and Go, and I also have experience with JavaScript."},
            {"role": "interviewer", "content": "Why do you want to work at our company?"},
            {"role": "candidate", "content": "I admire your focus on AI research and want to contribute to your open-source projects."}
        ]

    generate_report(conversation)
