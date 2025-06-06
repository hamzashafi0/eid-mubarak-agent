import streamlit as st
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Page setup
st.set_page_config(page_title="Eid Mubarak Agent", page_icon="🕌")

# Validate API key
if not gemini_api_key:
    st.error("Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# Initialize external model client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Define the model
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

# Run configuration
config = RunConfig(model=model, model_provider=external_client)

# Define the Agent
eid_agent = Agent(
    name="Eid Mubarak Agent",
    instructions="You are an Eid Mubarak agent. Wish Eid-ul-Adha Mubarak in a mix of Urdu and English. Include the Islamic meaning of this Eid. Use emojis like 🕌✨🐐🌙❤.",
    model=model
)

# Custom CSS
st.markdown("""
    <style>
        body { background-color: #f0f4f8; }
        .stTextInput>div>div>input {
            padding: 10px;
            border: 2px solid #800080;
            border-radius: 10px;
            font-size: 16px;
        }
        .stButton>button {
            background-color: purple;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #D8BFD8;
        }
    </style>
""", unsafe_allow_html=True)

# UI Header
st.markdown("<h1 style='color: purple;'>Eid Mubarak Message Agent 🐫</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color: purple;'>Eid-ul-Adha Mubarak! 🐐✨</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: purple;'>Create a personalized Eid message with the help of AI! 🌙🐐🐪</p>", unsafe_allow_html=True)

# Input
name = st.text_input("Enter your name:")

# Async function wrapped for Streamlit compatibility
def generate_sync_message(user_name):
    return asyncio.run(generate_message(user_name))

async def generate_message(user_name):
    response = await Runner.run(
        eid_agent,
        f"Write a sweet Eid-ul-Adha message for {user_name}",
        run_config=config
    )
    return response.final_output

# Generate button
if st.button("🐐 Generate Eid Message"):
    if name:
        with st.spinner("AI message taiyar ho raha hai..."):
            try:
                final_msg = generate_sync_message(name)
                st.success("🎊 Aap ka Eid Mubarak message:")
                st.text_area("Your Eid Message:", value=final_msg, height=200)
                st.balloons()
            except Exception as e:
                st.error(f"Kuch ghalat hogaya: {e}")
    else:
        st.warning("Please enter your name.")

# Footer
st.markdown("---")
st.markdown("<h3 style='color: purple;'>Built by Hamza Shafi ❤</h3>", unsafe_allow_html=True)
