import streamlit as st
import random
from datetime import datetime, date
import hashlib
import os
import json
import pandas as pd

# --- Page Config ---
st.set_page_config(
    page_title="Math Pro Marathon",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Constants & Setup ---
RESULTS_DIR = "results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

# --- Helper Functions ---
def cyrb53(s: str):
    """Fast, simple 53-bit string hash."""
    h1 = 0xdeadbeef
    h2 = 0x41c6ce57
    for ch in s:
        h1 = (h1 ^ ord(ch)) * 2654435761
        h2 = (h2 ^ ord(ch)) * 1597334677
    h1 = (h1 ^ (h1 >> 16)) * 2246822507
    h2 = (h2 ^ (h2 >> 13)) * 3266489909
    h1 = h1 & 0xFFFFFFFF
    h2 = h2 & 0xFFFFFFFF
    return (h1 << 5) + (h2 >> 27)

def format_duration(td):
    """Formats a timedelta object into a human-readable string."""
    minutes, seconds = divmod(td.total_seconds(), 60)
    return f"{int(minutes)}m {int(seconds)}s"

def generate_question(operands, min_bound, max_bound, seeded_random, no_regrouping=False):
    """Generates a single question, respecting the bounds for the answer."""
    max_attempts = 1000  # Avoid infinite loops for impossible bounds
    for _ in range(max_attempts):
        operand = seeded_random.choice(operands)
        question_text, answer = "", 0

        if operand == "+":
            if no_regrouping:
                # No regrouping addition: ensure units digit sum <= 9
                a_units = seeded_random.randint(0, 9)
                b_units = seeded_random.randint(0, 9 - a_units)  # Ensure sum <= 9
                a_tens = seeded_random.randint(0, 9)
                b_tens = seeded_random.randint(0, 9 - a_tens)  # Ensure sum <= 9
                
                a = a_tens * 10 + a_units
                b = b_tens * 10 + b_units
                # Ensure numbers are positive and reasonable
                if a == 0: a = seeded_random.randint(1, 9)
                if b == 0: b = seeded_random.randint(1, 9)
            else:
                a = seeded_random.randint(1, 100)
                b = seeded_random.randint(1, 100)
            
            answer = a + b
            question_text = f"{a} + {b}"
            
        elif operand == "-":
            if no_regrouping:
                # No regrouping subtraction: ensure top digit >= bottom digit in each column
                a_units = seeded_random.randint(0, 9)
                b_units = seeded_random.randint(0, a_units)  # Ensure a_units >= b_units
                a_tens = seeded_random.randint(0, 9)
                b_tens = seeded_random.randint(0, a_tens)  # Ensure a_tens >= b_tens
                
                a = a_tens * 10 + a_units
                b = b_tens * 10 + b_units
                # Ensure numbers are positive and a > b
                if a == 0: a = seeded_random.randint(1, 99)
                if b == 0: b = seeded_random.randint(1, min(9, a-1))
                if a <= b: 
                    # Swap if needed to ensure a > b
                    a, b = b, a
            else:
                a = seeded_random.randint(1, 100)
                b = seeded_random.randint(1, a)
            
            answer = a - b
            question_text = f"{a} - {b}"
            
        elif operand == "×":
            a = seeded_random.randint(2, 12)
            b = seeded_random.randint(2, 12)
            answer = a * b
            question_text = f"{a} × {b}"
        elif operand == "÷":
            multiplier = seeded_random.randint(2, 12)
            b = seeded_random.randint(2, 12)
            a = b * multiplier
            answer = multiplier
            question_text = f"{a} ÷ {b}"
        elif operand == "x²":
            a = seeded_random.randint(2, 20)
            answer = a * a
            question_text = f"{a}²"
        elif operand == "xʸ":
            base = seeded_random.randint(2, 10)
            power = seeded_random.randint(2, 4)
            answer = base ** power
            question_text = f"{base} ^ {power}"

        if min_bound <= answer <= max_bound:
            return {"text": question_text, "answer": answer}
            
    # If max attempts reached, return a fallback question
    return {"text": "1 + 1", "answer": 2}


# --- History Management ---
def save_result_to_disk(result_data):
    """Saves a single quiz result to a timestamped JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filepath = os.path.join(RESULTS_DIR, f"result_{timestamp}.json")
    with open(filepath, 'w') as f:
        json.dump(result_data, f, indent=4)

def load_history_from_disk():
    """Loads all quiz results from the results directory."""
    history = []
    for filename in sorted(os.listdir(RESULTS_DIR), reverse=True):
        if filename.endswith(".json"):
            filepath = os.path.join(RESULTS_DIR, filename)
            try:
                with open(filepath, 'r') as f:
                    history.append(json.load(f))
            except (json.JSONDecodeError, IOError):
                st.warning(f"Could not read or parse result file: {filename}")
    return history

def clear_history_from_disk():
    """Deletes all result files from the results directory."""
    for filename in os.listdir(RESULTS_DIR):
        os.remove(os.path.join(RESULTS_DIR, filename))
    st.toast("History cleared!", icon="🧹")


# --- Session State Initialization ---
def init_session_state():
    """Initialize non-persistent session state variables."""
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_complete' not in st.session_state:
        st.session_state.quiz_complete = False
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'correct_count' not in st.session_state:
        st.session_state.correct_count = 0
    if 'wrong_count' not in st.session_state:
        st.session_state.wrong_count = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}

init_session_state()

# --- UI: Sidebar, Main Logic, etc. (with modifications) ---

# (CSS injection for sidebar hiding remains the same)
if st.session_state.quiz_started and not st.session_state.quiz_complete:
    st.markdown("""<style>[data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}</style>""", unsafe_allow_html=True)

# (Sidebar settings remain the same)
with st.sidebar:
    st.title("⚙️ Settings")
    def sync_slider(): st.session_state.slider = st.session_state.num_input
    def sync_num_input(): st.session_state.num_input = st.session_state.slider
    with st.expander("Quiz Setup", expanded=True):
        operand_options = ["+", "-", "×", "÷", "x²", "xʸ"]
        selected_operands = st.multiselect("Select Operands:", options=operand_options, default=["+", "-"])
        st.write("Number of Questions:")
        if 'num_input' not in st.session_state: st.session_state.num_input = 10
        if 'slider' not in st.session_state: st.session_state.slider = 10
        st.number_input("Or type a number", min_value=1, max_value=100, key="num_input", on_change=sync_slider)
        st.slider(" ", min_value=1, max_value=100, key="slider", on_change=sync_num_input)
        quiz_length = st.session_state.num_input
    with st.expander("Answer Bounds", expanded=True):
        st.write("Bounds for Answers:")
        c1, c2 = st.columns(2)
        lower_bound = c1.number_input("Min Answer", value=0, min_value=-1000, max_value=1000)
        upper_bound = c2.number_input("Max Answer", value=100, min_value=-1000, max_value=1000)
    
    with st.expander("Learning Options", expanded=True):
        st.write("For younger learners:")
        no_regrouping = st.checkbox("No Regrouping (No Carrying/Borrowing)", help="Only generates addition/subtraction problems that don't require carrying or borrowing")
    
    if not selected_operands: st.warning("Please select at least one operand."); st.stop()
    if lower_bound > upper_bound: st.warning("Min bound cannot exceed max."); st.stop()

def start_quiz():
    # Use the current time (down to the microsecond) as a seed for true randomness on every take.
    random_seed_str = datetime.now().isoformat()
    seed_value = cyrb53(random_seed_str)
    seeded_random = random.Random(seed_value)

    st.session_state.questions, generated_texts = [], set()
    while len(st.session_state.questions) < quiz_length:
        q = generate_question(selected_operands, lower_bound, upper_bound, seeded_random, no_regrouping)
        if q['text'] not in generated_texts: st.session_state.questions.append(q); generated_texts.add(q['text'])
    st.session_state.quiz_started = True
    st.session_state.quiz_complete = False
    st.session_state.current_question_index = 0
    st.session_state.correct_count = 0
    st.session_state.wrong_count = 0
    st.session_state.user_answers = {}
    st.session_state.start_time = datetime.now()

def reset_quiz():
    # ... (reset_quiz logic is the same)
    st.session_state.quiz_started = False
    st.session_state.quiz_complete = False
    # Re-initialize to clear quiz-specific data
    for key in ['questions', 'current_question_index', 'correct_count', 'wrong_count', 'user_answers', 'start_time']:
        if key in st.session_state:
            del st.session_state[key]
    init_session_state()

def process_answer():
    """Process the user's answer and move to the next question or finish the quiz."""
    idx = st.session_state.current_question_index
    question = st.session_state.questions[idx]
    
    # Get the answer from the input field
    user_val = st.session_state[f"ans_input_{idx}"]

    if user_val is not None:
        st.session_state.user_answers[idx] = user_val
        
        # Check answer
        if user_val == question['answer']:
            st.session_state.correct_count += 1
            st.toast("Correct! 🎉")
        else:
            st.session_state.wrong_count += 1
            st.toast(f"Wrong. Answer was {question['answer']}.")
        
        # Move to next question or finish quiz
        if st.session_state.current_question_index + 1 < quiz_length:
            st.session_state.current_question_index += 1
            st.rerun()  # Force immediate rerun to show next question
        else:
            st.session_state.quiz_complete = True
            # --- DURATION CALCULATION ---
            end_time = datetime.now()
            duration = end_time - st.session_state.start_time
            duration_str = format_duration(duration)
            st.session_state.last_duration = duration_str # Save for immediate display
            # --- END DURATION CALCULATION ---
            score = round((st.session_state.correct_count / quiz_length) * 100)
            result_data = {
                "Date": end_time.strftime("%Y-%m-%d %H:%M"),
                "Score": f"{score}%",
                "Tally": f"{st.session_state.correct_count}/{quiz_length}",
                "Duration": duration_str,
                "Operands": ", ".join(selected_operands)
            }
            save_result_to_disk(result_data)
            st.rerun()  # Force immediate rerun to show completion screen
    else:
        st.toast("Please enter an answer.")

st.title("Math Pro Marathon")

if not st.session_state.quiz_started:
    st.header("Welcome!")
    st.write("Adjust settings and click 'Start Quiz'.")
    if st.button("Start Quiz", type="primary"):
        start_quiz()
        st.rerun()

elif not st.session_state.quiz_complete:
    # ... (Header, metrics are the same)
    st.header(f"Question {st.session_state.current_question_index + 1} of {quiz_length}")
    c1, c2 = st.columns(2)
    c1.metric("✅ Correct", st.session_state.correct_count)
    c2.metric("❌ Wrong", st.session_state.wrong_count)
    question = st.session_state.questions[st.session_state.current_question_index]
    st.subheader(f"What is {question['text']}?")

    with st.form(key="answer_form", clear_on_submit=True, enter_to_submit=True):
        user_answer = st.number_input("Your Answer:", value=None, step=1, key=f"ans_input_{st.session_state.current_question_index}")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            process_answer()
    
    if st.button("Quit Quiz"):
        reset_quiz()
        st.rerun()

elif st.session_state.quiz_complete:
    # ... (Quiz complete screen is mostly the same)
    st.header("🏁 Quiz Complete!")
    st.balloons()
    score = round((st.session_state.correct_count / quiz_length) * 100)
    st.subheader(f"Final Score: {score}%")

    # Display Tally and Duration
    col1, col2 = st.columns(2)
    col1.metric("Tally", f"{st.session_state.correct_count}/{quiz_length}")
    if 'last_duration' in st.session_state:
        col2.metric("Time Taken", st.session_state.last_duration)

    st.write("---")
    st.subheader("Your Results:")
    for i, q in enumerate(st.session_state.questions):
        ans = st.session_state.user_answers.get(i, "N/A")
        icon = "✅" if ans == q['answer'] else "❌"
        st.write(f"{i+1}. {q['text']} = {q['answer']} (You: {ans}) {icon}")
    if st.button("Play Again", type="primary"):
        reset_quiz()
        st.rerun()

# --- UI: History Display (Now reads from disk) ---
st.write("---")
st.header("📜 Past Results")
history_data = load_history_from_disk()

if not history_data:
    st.info("No past results found. Complete a quiz to see your history here.")
else:
    # Use pandas for better table display
    df = pd.DataFrame(history_data)
    st.dataframe(df, use_container_width=True)

    with st.expander("⚠️ Clear History"):
        st.warning("This will permanently delete all saved results. This action cannot be undone.")
        if st.button("Yes, I'm sure, delete all history"):
            clear_history_from_disk()
            st.rerun()
