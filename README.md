# Cosmos Dental Clinic Chatbot

An AI-powered dental clinic assistant built with Streamlit and the Groq API. Patients can book, reschedule, and cancel appointments through a conversational chat interface.

## Features
- Book, reschedule, and cancel appointments via natural conversation
- Symptom triage to direct patients to the right care level
- Pre-appointment preparation instructions
- General dental FAQ answering
- Appointments saved locally to a JSON file

## Tech Stack
- Python
- Streamlit
- Groq API (LLaMA 3.3 70b)
- python-dotenv

## How It Works
The chatbot uses a structured prompt with clinic information injected directly — no RAG needed since the knowledge base is small enough to fit in the system prompt. Appointment management works via a custom ACTION pattern: the LLM outputs a structured tag when a booking action is needed, which Python parses and writes to a local JSON file.

## Run Locally
1. Clone the repository
2. Install dependencies
3. create a .env file in the project folder containing your GROQ_API_KEY
4. type in the terminal to open:
streamlit run "chatbot code.py"


## Live Demo
[Click here](https://exo-k2-18b-cosmos-dental-clinic-chatbot-chatbotcode-iwdyvn.streamlit.app/)
