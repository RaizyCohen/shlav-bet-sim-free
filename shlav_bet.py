# Shlav Bet Simulator - Proof of Concept (with Streamlit UI)

# 1. Backend + Frontend Setup
import random
import streamlit as st
from typing import List
import openai

# Configure OpenAI
openai.api_key = "your_openai_api_key"

# 2. Prompts and Memory Store
CASE_MEMORY = {}

SYSTEM_PROMPT_CASE_GENERATOR = """
You are a board-certified internal medicine specialist.
Generate a realistic oral exam case for the Israeli 'Shlav Bet'.
Include:
1. Chief complaint and history
2. Vital signs
3. Initial context
Only output the case text.
"""

SYSTEM_PROMPT_PATIENT_SIMULATOR = """
You are a simulated patient case for a residency exam. Respond only with what the case allows: history, vitals, results of tests that have been ordered. Do not give away the diagnosis. Keep it realistic.
"""

SYSTEM_PROMPT_EVALUATOR = """
You are an internal medicine examiner.
Evaluate the resident's reasoning based on their responses.
Score on differential diagnosis, test ordering, and final diagnosis. Return a brief analysis.
"""

# 3. Helper Functions
def generate_case(difficulty: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_CASE_GENERATOR},
            {"role": "user", "content": f"Generate a {difficulty} case."}
        ]
    )
    return response.choices[0].message["content"]

def get_simulation_response(case_text: str, user_input: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_PATIENT_SIMULATOR},
            {"role": "user", "content": f"Case: {case_text}\nResident: {user_input}"}
        ]
    )
    return response.choices[0].message["content"]

def evaluate_resident(case_text: str, dialog_history: List[str]) -> str:
    history = "\n".join(dialog_history)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_EVALUATOR},
            {"role": "user", "content": f"Case: {case_text}\nResident Dialogue:\n{history}"}
        ]
    )
    return response.choices[0].message["content"]

# 4. Streamlit UI
st.title("Shlav Bet Internal Medicine Simulator")

if "case_id" not in st.session_state:
    st.session_state.case_id = ""
    st.session_state.case_text = ""
    st.session_state.dialog = []

st.sidebar.header("1. Case Generation")
difficulty = st.sidebar.selectbox("Select difficulty", ["easy", "medium", "hard"])
if st.sidebar.button("Generate New Case"):
    case_text = generate_case(difficulty)
    case_id = f"case_{random.randint(1000, 9999)}"
    st.session_state.case_id = case_id
    st.session_state.case_text = case_text
    st.session_state.dialog = []

if st.session_state.case_text:
    st.subheader("🩺 Case Presentation")
    st.text_area("Case", value=st.session_state.case_text, height=200)

    st.subheader("🗣️ Resident Interaction")
    user_input = st.text_input("Ask questions, order tests, make a diagnosis:")
    if st.button("Submit Question/Action") and user_input:
        response = get_simulation_response(st.session_state.case_text, user_input)
        st.session_state.dialog.append(f"Resident: {user_input}\nAI: {response}")
        st.success("AI Response: ")
        st.write(response)

    if st.session_state.dialog:
        st.subheader("💬 Dialogue History")
        for exchange in st.session_state.dialog:
            st.text(exchange)

    if st.button("🧾 Evaluate Performance"):
        eval_text = evaluate_resident(st.session_state.case_text, st.session_state.dialog)
        st.subheader("✅ Evaluation Result")
        st.write(eval_text)

else:
    st.info("Please generate a case from the sidebar to begin.")

