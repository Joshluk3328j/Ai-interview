# 🧠 AI Interview System for Rehabilitation

This project is an **AI-powered interviewer platform**, ViewHire designed to conduct structured, empathetic, and insightful interviews — particularly for use in. It combines real-time avatar interaction, voice and text input, transcript tracking, and automated evaluation to help assess communication skills, emotional readiness, and personal growth.

Built with **Next.js**, **TypeScript**, and **Python**, the system integrates the **HeyGen streaming avatar SDK**, **Hugging Face models**, and **PDF generation tools** to deliver a complete interview experience and post-session analysis.

![Interview Interface](https://github.com/Joshluk3328j/Ai-interview/blob/main/public/demo.png?raw=true)

---

## 🎯 Purpose

This platform was developed as part of a rehabilitation initiative to:

- Help facilitators assess progress in communication, confidence, and clarity.
- Generate structured transcripts and evaluations for review and documentation.

---

## 🚀 Features

- Real-time AI avatar interviewer (via HeyGen SDK)
- Voice and text input support
- Live transcript tracking with speaker labels
- Summarized transcript generation
- Automated evaluation using NLP models
- PDF report export (transcript + evaluation)
- Secure token-based session authentication
- Modular backend with Python integration

---

## 🛠️ Technologies Used
| Frontend | Backend | AI Modules | PDF Generation | Avatar Streaming | Evaluation Logic|
|----------|---------|------------|----------------|------------------|-----------------|
| React 19 | Node.js | Hugging Face Transformers| Report Lab| Heygen SDK| Custom rubric scoring via python
| TailwindCSS | Typescript|------------|----------------|------------------|-----------------|
| Next.js | Python 3.10 |------------|----------------|------------------|-----------------|

---

## 🧪 How It Works

1. **User starts a session** by selecting an avatar, language, and voice settings.
2. **Live interview begins** — user interacts via voice or text.
![Live Interview](C:\Users\Sulaiman Abukakar\Desktop\MELA's PROJECT\Ai-interview\Screenshot from 2025-08-16 10-45-59.png "Live Interview")

3. **Transcript is built** in real time, capturing both user and avatar turns.
4. **Session ends** — user clicks the “X” button.
5. **Backend finalizes transcript**, runs summarization and evaluation.
6. **Frontend displays summary**: a readable transcript + rubric-based scores.
7. **User downloads PDF report** for documentation or review.

---


