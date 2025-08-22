# 🧠 ViewHire - AI Interview System for Remote Hiring

This project is an **AI-powered interviewer platform**, ViewHire designed to conduct structured, professional, and insightful interviews — particularly for use in HR. It combines real-time avatar interaction, voice and text input, transcript tracking, and automated evaluation to help assess communication skills, emotional readiness, personal growth, and career relevance.

Built with **Next.js**, **TypeScript**, and **Python**, the system integrates the **HeyGen streaming avatar SDK**, **Hugging Face models**, and **PDF generation tools** to deliver a complete interview experience and post-session analysis for informed decision making.

---

## 🎯 Purpose

This platform was developed as part of a initiative to improve hiring process for HR with Real-Time Automated Interviewer (RTAI):

- Realtime conversational interview with the AI system.
- Candidates are been asked structured questions and with options to ask questions where they're not clear on questions asked or may ask questions for clarity.
- System detects when there are multiple heads in the frame during an interview.
- A start meeting with candidate registration to receive and check candidates data for validity.
- The system autostop meetings when time allocated lapse.
- Generates structured transcripts and evaluations for review and documentation.
- Help the hiring team assess candidates suitability via communication, confidence, and clarity at expressing themselves.

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

![Interview Interface](https://github.com/Joshluk3328j/Ai-interview/blob/main/public/demo2.png?raw=true)

2. **Live interview begins** — user interacts via voice or text.

![Interview Interface](https://github.com/Joshluk3328j/Ai-interview/blob/main/public/demo.png?raw=true)

3. **Transcript is built** in real time, capturing both user and avatar turns.
4. **Session ends** — user clicks the “X” button.
5. **Backend finalizes transcript**, runs summarization and evaluation.
6. **Frontend displays summary**: a readable transcript + rubric-based scores.
7. **User downloads PDF report** for documentation or review.

---








