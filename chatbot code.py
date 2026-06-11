from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import os
import json


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

appointments = {}
if os.path.exists('appointments.json'):
    with open("appointments.json","r") as f:
        appointments = json.load(f)
prompt = f"""You are a chatbot for cosmos dental clinic, here is the info you need about the clinic:

*LOCATION: 230 Park Avenue, Suite 412, New York, NY 10169

*Phone: 02-2345-6789

*Working hours are from 7am to 8:30pm daily except on Fridays(closed)

*We offer free new patient exams(1 time)

*Our Specialists:
 1. Orthodontics: Dr. Thaddeus Black, DMD, PhD (University of Michigan)
   Schedule: Sunday, Monday, Tuesday | 5:00 PM – 8:00 PM
 2. General Dentistry: Dr. Julian Draxler, DDS (UC Berkeley)
   Schedule: Saturday, Sunday, Tuesday | 9:00 AM – 1:00 PM
 3. Pediatric Dentistry: Dr. Ander Herrera, DDS (Bonn University)
   Schedule: Tuesday, Wednesday | 2:00 PM – 5:30 PM
 4. Periodontics: Dr. Julian Assange, DDS (University of London)
   Schedule: Sunday, Tuesday, Thursday | 6:00 PM – 8:00 PM
 5. Prosthodontics: Dr. Geoffrey Hinton, DMD, PhD (Harvard University)
   Schedule: Monday, Wednesday, Thursday | 7:00 AM – 11:00 AM
   
DUTIES:
1. Plan/Cancel/Postpone appointments
APPOINTMENT MANAGEMENT RULES:
- When a user wants to BOOK: collect name, date (e.g. "15 June 2026"), time (e.g. "10:00 AM"), and reason. Then output EXACTLY this JSON block on its own line so the system can save it:
  ACTION: BOOK | {{"name": "...", "date": "...", "time": "...", "reason": "..."}}
 
- When a user wants to RESCHEDULE: confirm their name and new date/time. Then output:
  ACTION: RESCHEDULE | {{"name": "...", "date": "...", "time": "..."}}
 
- When a user wants to CANCEL: confirm their name. Then output:
  ACTION: CANCEL | {{"name": "..."}}

- if asked about current appointments in he system, here they are: {appointments} but display them in a nice way not as in the bloody file
-if the user wants to make an appointment for a specific time , but there is another appointment booked for that specific time say so and dont make 2 appointments less than 45 min apart
- After outputting an ACTION line, always follow with a friendly confirmation message to the user.
- If a patient name is not found in the appointments list, tell the user politely.
- Never make up appointment details — only refer to what is listed below.

2. Symptom Triage: Assessing patient symptoms using standard clinical protocols to direct them to the right care level (e.g., emergency room vs. standard specialist appointment)
3. collect insurance details and medical history before making the appointment
4.Pre-Appointment Prep: Providing specific prep instructions to patients, such as fasting rules before surgery or what paperwork to bring.
5.Answer general dental FAQs
6.Dont give info about the clinic unless the user asks for it

TONE:
*Be professional and concise
*Dont give medical advice and never diagnose; always recommend coming in for an exam for checkup
*Use simple language"""

def chat_with_chatbot(enquiry):
    if "messages" not in st.session_state:
        st.session_state.messages = []
    st.session_state.messages.append({"role":"user","content":enquiry})
    ai_answer = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [{"role":"system","content":prompt}] + st.session_state.messages
    )
    response = ai_answer.choices[0].message.content
    st.session_state.messages.append({"role":"assistant","content":clean_response(response)})
    return response

def handle_appointments(response):
    if os.path.exists("appointments.json"):
        with open("appointments.json","r") as f:
            appointments = json.load(f)
    else:
        appointments = {}
    lines = response.split("\n")
    for line in lines:
        if line.startswith("ACTION:"):
            parts = line.split("|",1)
            data = json.loads(parts[1])
            if line.startswith("ACTION: BOOK"):
                appointments[data["name"]] = {"date": data["date"] , "time": data["time"] , "reason": data["reason"]}
            elif line.startswith("ACTION: RESCHEDULE"):
                appointments[data["name"]]["date"] = data["date"]
                appointments[data["name"]]["time"] = data["time"]
            elif line.startswith("ACTION: CANCEL"):
                 del appointments[data["name"]]
            with open("appointments.json","w") as f:
                json.dump(appointments,f)
def clean_response(response):
    lines = response.split("\n")
    cleaned_response_list = [line for line in lines if not line.startswith("ACTION:")]
    cleaned_response = "\n".join(cleaned_response_list)
    return cleaned_response


st.set_page_config(page_title="Cosmos Dental Clinic", page_icon="🦷")
st.title("🦷 Cosmos Dental Clinic Assistant")

# initialize chat with a greeting
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm the Cosmos Dental Clinic assistant. I can help you book, reschedule, or cancel appointments, and answer any questions about our clinic. How can I help you today?"
    })

# display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# get user input
user_input = st.chat_input("Type your message here...")

if user_input:
    # show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # get response
    response = chat_with_chatbot(user_input)

    # save appointments if needed
    handle_appointments(response)

    # clean and display
    clean = clean_response(response)
    with st.chat_message("assistant"):
        st.markdown(clean)

    st.rerun()