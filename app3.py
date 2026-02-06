import streamlit as st
import pandas as pd
import joblib
import base64
import time
import google.generativeai as genai

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
API_KEY = "AIzaSyC5gen4OcnimhwWonkmbyJ39xOQ3EyS1dU"
genai.configure(api_key=API_KEY)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Affordable Energy Saver – Rural Development",
    page_icon="⚡",
    layout="centered"
)

# --------------------------------------------------
# GEMINI SMART ENERGY BOT LOGIC
# --------------------------------------------------
def smart_energy_bot(user_input, prediction):
    if prediction == 1:
        grid_context = "The current energy demand is HIGH. Advise immediate load shifting and battery usage."
    elif prediction == 0:
        grid_context = "The current energy demand is NORMAL. Advise routine maintenance and efficiency."
    else:
        grid_context = "System is in ready state."

    system_prompt = f"""
    You are an intelligent 'Affordable Energy Saver' assistant designed for rural development.
    
    CURRENT GRID STATUS: {grid_context}
    
    YOUR RULES:
    1. You must ONLY answer questions related to energy, electricity, solar power, batteries, smart grids, and power saving.
    2. If the user asks about anything else, politely refuse.
    3. Keep your answers concise (under 3 sentences) and easy to understand.
    4. Provide actionable advice based on the Current Grid Status.
    
    User Question: {user_input}
    """

    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --------------------------------------------------
# BACKGROUND IMAGE
# --------------------------------------------------
def set_bg(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        pass 

set_bg("Background.png")

# --------------------------------------------------
# CUSTOM CSS (ROBOT MOVED TO RIGHT SIDE)
# --------------------------------------------------
st.markdown("""
<style>
.card {
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(12px);
    padding: 28px;
    border-radius: 22px;
    box-shadow: 0px 10px 40px rgba(0,0,0,0.35);
    margin-bottom: 25px;
    color: white;
}

h1,h2,h3 { text-align:center; color:white; }

section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.8);
}

/* 🟢 FLOATING ROBOT CONTAINER (RIGHT SIDE) */
[data-testid="stPopover"] {
    position: fixed;
    bottom: 40px;
    right: -1040px;   /* ✅ MOVED TO RIGHT */
    z-index: 999999;
}
  /* Main robot button */
[data-testid="stPopover"] > div > button {
    width: 96px;
    height: 96px;
    border-radius: 50%;
    border: none;
    cursor: pointer;

    /* Robot GIF */
    background-image: url("https://media.tenor.com/CigpzapemsoAAAAi/hi-robot.gif");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-color: transparent;

   
}

/* Hide default text */
[data-testid="stPopover"] > div > button span,
[data-testid="stPopover"] > div > button div {
    display: none !important;
}



/* Hover = stronger energy */
[data-testid="stPopover"] > div > button:hover {
    transform: scale(1.15);
    animation-play-state: paused;
}

/* ===============================
   🎞️ ANIMATIONS
================================ */

@keyframes aiGlow {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes aiFloat {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}
/* 🟢 "HELLO" SPEECH BUBBLE */
[data-testid="stPopover"]::after {
    content: "EcoGrid AI";
    position: absolute;
    bottom: 110px;
    right: 1160px;
    background: linear-gradient(135deg,#22c55e,#4ade80);
    color: #062e1f;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    box-shadow: 0 8px 20px rgba(0,0,0,0.35);
}

@keyframes floatHello {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.bot-speech {
    background: #e1ffef;
    color: #0b3d25;
    padding: 12px;
    border-radius: 12px;
    border-left: 4px solid #2EE59D;
    margin-top: 10px;
}

.footer {
    text-align:center;
    color:#dddddd;
    font-size:14px;
    margin-top:30px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------
@st.cache_resource
def load_model():
    try:
        model = joblib.load("high_demand_classifier.pkl")
        features = joblib.load("model_features.pkl")
        return model, features
    except:
        return None, None

model, feature_names = load_model()

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("""
<h1>⚡ Affordable Energy Saver</h1>
<h3>Smart Grid Energy Demand Prediction 🌱</h3>
<p>Empowering Sustainable Rural Development using Green AI</p>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR INPUTS
# --------------------------------------------------
st.sidebar.header("⚙️ Smart Grid Inputs")

temperature = st.sidebar.number_input("🌡️ Temperature (°C)", 0.0, 60.0, 30.0)
humidity = st.sidebar.number_input("💧 Humidity (%)", 0.0, 100.0, 60.0)
hour = st.sidebar.slider("⏰ Hour of Day", 0, 23, 18)

voltage = st.sidebar.number_input("🔌 Voltage (V)", 180.0, 260.0, 230.0)
current = st.sidebar.number_input("⚡ Current (A)", 0.0, 50.0, 10.0)
power_factor = st.sidebar.slider("📊 Power Factor", 0.0, 1.0, 0.95)

renewable = st.sidebar.number_input("☀️ Renewable Energy (kW)", 0.0, 100.0, 12.0)
battery = st.sidebar.slider("🔋 Battery Level (%)", 0.0, 100.0, 70.0)

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🔮 Energy Demand Prediction")

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if st.button("🔍 Predict Energy Demand"):
    if model:
        with st.spinner("⚡ Analyzing smart grid data..."):
            time.sleep(1.5)

        input_data = pd.DataFrame([{
            'temperature_C': temperature,
            'humidity_percent': humidity,
            'hour': hour,
            'voltage_V': voltage,
            'current_A': current,
            'power_factor': power_factor,
            'distributed_generation_kW': renewable,
            'battery_storage_level_%': battery
        }])

        st.session_state.prediction_result = model.predict(input_data)[0]
    else:
        st.error("Model file not found.")

if st.session_state.prediction_result is not None:
    if st.session_state.prediction_result == 1:
        st.error("⚠️ HIGH ENERGY DEMAND EXPECTED")
    else:
        st.success("✅ NORMAL ENERGY DEMAND")

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# FLOATING ROBOT CHATBOT (RIGHT SIDE)
# --------------------------------------------------
with st.popover("🤖"):
    st.markdown("### 🤖 Energy Assistant")
    st.image("https://media.tenor.com/Goody_6dCQAAAAAC/hi-robot.gif", width=100)
    st.write("I am here to help with your energy questions!")

    if "bot_message" not in st.session_state:
        st.session_state.bot_message = "Hello! Ask me about saving power or battery usage."

    user_query = st.text_input("Type your question here:", key="floating_chat_input")

    if st.button("Send 🚀", key="send_btn"):
        if user_query:
            pred = st.session_state.get('prediction_result', None)
            with st.spinner("Thinking..."):
                st.session_state.bot_message = smart_energy_bot(user_query, pred)

    st.markdown(f"""
    <div class="bot-speech">
        <b>AI:</b> {st.session_state.bot_message}
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div class="footer">
🌱 Smart Grid Energy Management | Green AI Project <br>
Designed for Sustainable Rural Development
</div>
""", unsafe_allow_html=True)
