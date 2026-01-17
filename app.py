import streamlit as st
import google.generativeai as genai
import time
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="DECISION ENGINE", page_icon="💣", layout="centered")

# --- CSS STYLING (Dark/Hacker Vibe) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1 { font-family: 'Courier New', monospace; color: #ff4b4b; text-align: center; }
    .stTextArea textarea { background-color: #262730; color: white; border-radius: 5px; }
    .stButton>button {
        width: 100%; background-color: #ff4b4b; color: white; border: none;
        height: 50px; font-weight: bold; letter-spacing: 2px;
    }
    .stRadio>div {flex-direction: row;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- API SETUP (SECURE WAY) ---
# Ye line check karegi ki key 'Secrets' mein hai ya nahi
api_key = st.secrets.get("AIzaSyA-b6k5nUVB8KPybhvFMVlMFvxp1Ax9AvM")

if not api_key:
    st.error("⚠️ API Key Missing! Setup instructions: Streamlit Cloud Settings > Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- BRAIN FUNCTION ---
def get_brutal_decision(problem, time_pressure, fear):
    prompt = f"""
    Act as the 'AI Overthinker Decision Tool'. 
    Persona: Brutal, Logic-driven, Gen Z big brother.
    Language: Hinglish (Casual, Slang allowed).

    User Problem: {problem}
    Time Pressure: {time_pressure}
    Fear: {fear}

    Task:
    1. Expose the hidden excuse (laziness/ego).
    2. Provide EXACTLY 2 Options (A vs B).
    3. Force a decision based on logic/regret minimization.
    4. Give ONE specific, uncomfortable 24-hour action.

    Format (Markdown):
    ### 💣 TRUTH BOMB
    [Brutal Truth]

    ### ⚖️ OPTIONS
    **A) [Option A]**
    - Risk: ...
    - Outcome: ...

    **B) [Option B]**
    - Risk: ...
    - Outcome: ...

    ### 🔨 VERDICT
    **Choose [A/B]** because...

    ### ⚡ ACTION (Next 24h)
    [Action]
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "⚠️ Error: API Limit or Connection issue."

# --- UI LAYOUT ---
st.title("STOP LOOPING. DECIDE.")

problem = st.text_area("What are you stuck on?", placeholder="e.g. Drop year vs College, Breakup vs Stay...")

col1, col2 = st.columns(2)
with col1:
    time_pressure = st.selectbox("Time Pressure?", ["Today", "This Week", "No Rush"])
with col2:
    fear = st.text_input("Worst Fear?", placeholder="Log kya kahenge...")

if st.button("FORCE DECISION"):
    if not problem or not fear:
        st.warning("Darr mat. Pura likh.")
    else:
        # Animation
        bar = st.progress(0)
        status = st.empty()
        for i in range(100):
            time.sleep(0.01)
            bar.progress(i + 1)
            if i == 20: status.text("Removing emotions...")
            if i == 50: status.text("Calculating regret...")
            if i == 80: status.text("Finalizing verdict...")
        
        status.empty()
        bar.empty()

        # Output
        result = get_brutal_decision(problem, time_pressure, fear)
        st.markdown("---")
        st.markdown(result)
        st.markdown("---")
        
        st.caption("Built by XIZOA.")
