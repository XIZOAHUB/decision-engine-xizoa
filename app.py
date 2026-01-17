import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURATION ---
# 🔑 TERI API KEY (Hardcoded as requested)
API_KEY = "AIzaSyA-b6k5nUVB8KPybhvFMVlMFvxp1Ax9AvM"

# Setup Gemini
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ API Key Error: {e}")

# --- UI SETUP ---
st.set_page_config(page_title="DECISION ENGINE", page_icon="💣", layout="centered")

# --- CUSTOM CSS (PREMIUM DARK & SMOOTH) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Headings */
    h1 {
        font-family: 'Courier New', monospace;
        color: #ff4b4b;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 30px;
    }
    
    /* Inputs (Text Area & Input) */
    .stTextArea textarea, .stTextInput input {
        background-color: #1c1f26;
        color: #ffffff;
        border: 1px solid #30333d;
        border-radius: 8px; /* Smooth corners */
        font-family: 'Inter', sans-serif;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #ff4b4b;
        box-shadow: 0 0 5px rgba(255, 75, 75, 0.5);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff4b4b 0%, #ff1c1c 100%);
        color: white;
        border: none;
        border-radius: 8px;
        height: 55px;
        font-weight: bold;
        letter-spacing: 1px;
        font-size: 18px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
    }

    /* Radio Buttons */
    .stRadio > div {
        background-color: #1c1f26;
        padding: 10px;
        border-radius: 8px;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Truth Bomb Box Style */
    .truth-box {
        border-left: 5px solid #ff4b4b;
        background-color: #1c1f26;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- THE BRAIN (SYSTEM PROMPT) ---
def get_brutal_decision(problem, time_pressure, fear):
    prompt = f"""
    Act as the 'AI Overthinker Decision Tool'. 
    Persona: Brutally honest, logic-driven, Gen Z big brother. NO sympathy.
    Language: Hinglish (Hindi + English mix). Use slang like 'Scene ye hai', 'Bakchodi', 'Load mat le', 'Seedhi baat'.

    User Input:
    - Problem: {problem}
    - Time Pressure: {time_pressure}
    - Fear: {fear}

    Rules:
    1. Call out their excuse immediately.
    2. Give EXACTLY 2 Options (A vs B).
    3. Force a decision based on logic/regret minimization.
    4. Give one uncomfortable 24-hour action.

    Output Format (Strict Markdown):
    ### 💣 TRUTH BOMB
    [1 sentence brutal truth]

    ### ⚖️ YOUR ONLY OPTIONS
    **A) [Option A Name]**
    - Risk: [Risk]
    - Outcome: [6-month Reality]

    **B) [Option B Name]**
    - Risk: [Risk]
    - Outcome: [6-month Reality]

    ### 🔨 FORCED DECISION
    **Choose [A/B]** because [Reason].

    ### ⚡ NEXT 24 HOURS ACTION
    [Specific task. No 'think about it'. Action only.]
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"

# --- FRONTEND UI ---
st.title("STOP LOOPING. DECIDE.")

st.markdown("<p style='text-align: center; color: #888;'>Brutal Logic. Zero Fluff.</p>", unsafe_allow_html=True)
st.markdown("---")

# Input Section
col1, col2 = st.columns([2, 1])
with col1:
    problem = st.text_area("What are you stuck on?", placeholder="e.g. Drop year vs Private College...", height=120)
with col2:
    st.write("**Time Pressure?**")
    time_pressure = st.radio("Select one:", ["Today", "This Week", "No Rush"], label_visibility="collapsed")

fear = st.text_input("Worst fear if it goes wrong?", placeholder="e.g. Wasting a year, Parents kya bolenge...")

st.write("")
st.write("")

# Action Button
if st.button("FORCE DECISION 🚀"):
    if not problem or not fear:
        st.warning("⚠️ Darr mat. Problem aur Fear dono likh.")
    else:
        # Smooth Loading Animation
        progress_text = st.empty()
        bar = st.progress(0)
        
        stages = [
            "🧠 Reading your mind...", 
            "🔪 Cutting emotional noise...", 
            "⚖️ Weighing regrets...", 
            "🔥 Preparing Truth Bomb..."
        ]
        
        for i, stage in enumerate(stages):
            progress_text.markdown(f"**{stage}**")
            # Smoother progress bar movement
            for j in range(25):
                time.sleep(0.02) 
                bar.progress((i * 25) + j)
        
        bar.progress(100)
        time.sleep(0.5)
        progress_text.empty()
        bar.empty()

        # Generate Output
        result = get_brutal_decision(problem, time_pressure, fear)
        
        # Display Result with Custom Styling
        st.markdown(f"""
            <div class="truth-box">
                {result}
            </div>
        """, unsafe_allow_html=True)

        # Accountability Section
        st.write("---")
        st.markdown("<h4 style='text-align: center;'>Did you accept this?</h4>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        
        with c2:
            sub_c1, sub_c2 = st.columns(2)
            if sub_c1.button("✅ YES"):
                st.balloons()
                st.success("Good. Ab overthink mat kar. Kaam kar.")
            if sub_c2.button("❌ NO"):
                st.error("You are choosing to stay stuck.")

# Footer
st.markdown("<br><br><center><small style='color: #555;'>Built by XIZOA. Logic over Emotions.</small></center>", unsafe_allow_html=True)
