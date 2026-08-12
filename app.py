import streamlit as st
from google import genai

# Configure Gemini API
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# -----------------------------
# Page Title
# -----------------------------
st.title("AI Multiverse Chat")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("App Settings")

personalities = [
    "A friendly assistant",
    "A grumpy pirate captain",
    "A panicked college student at 3 AM",
    "A 1920s Mafia Boss",
    "A highly sarcastic fitness coach"
]

personality = st.sidebar.selectbox(
    "Choose a Personality",
    personalities
)

# -----------------------------
# Intensity Slider
# -----------------------------
intensity = st.sidebar.slider(
    "Intensity Level",
    1,
    10,
    5
)

# -----------------------------
# Dynamic Avatar
# -----------------------------
if personality == "A friendly assistant":
    bot_avatar = "🙂"

elif personality == "A grumpy pirate captain":
    bot_avatar = "🏴‍☠️"

elif personality == "A panicked college student at 3 AM":
    bot_avatar = "😱"

elif personality == "A 1920s Mafia Boss":
    bot_avatar = "🎩"

elif personality == "A highly sarcastic fitness coach":
    bot_avatar = "💪"

else:
    bot_avatar = "🤖"

# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:

    if msg["role"] == "assistant":
        with st.chat_message(
            "assistant",
            avatar=msg.get("avatar", bot_avatar)
        ):
            st.write(msg["content"])

    else:
        with st.chat_message("user"):
            st.write(msg["content"])

# -----------------------------
# User Input
# -----------------------------
user_input = st.chat_input("Type your message...")

# -----------------------------
# Generate Response
# -----------------------------
if user_input:

    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Prompt engineering
    ai_instructions = f"""
You are roleplaying as: {personality}.

Act out this personality at an intensity level of {intensity} out of 10.

1 means a very mild and subtle personality.
10 means an extreme, over-the-top embodiment of the personality.

Stay fully in character while answering the user.

User's message:
{user_input}
"""

    # Call Gemini
    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=ai_instructions
        )

        response_text = response.text

        # Display AI response
        with st.chat_message(
            "assistant",
            avatar=bot_avatar
        ):
            st.write(response_text)

        # Save AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "avatar": bot_avatar
        })

    except Exception as e:

        st.error(f"Gemini API Error: {e}") 
        