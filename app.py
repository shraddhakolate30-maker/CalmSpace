import streamlit as st
import requests

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="CalmSpace",
    page_icon="🧘",
    layout="centered"
)

# --------------------------------------------------
# CALMSPACE UI
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #88B5CC;
}

.block-container {
    max-width: 750px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

h1 {
    color: #29495C !important;
    text-align: center;
    font-size: 42px;
    font-weight: 700;
}

h2, h3 {
    color: #29495C !important;
}

p, label {
    color: #1F3545 !important;
}

.stTextArea textarea {
    background-color: #C9E2EE !important;
    color: #1F3545 !important;
    border: 1px solid #5D8FA8 !important;
    border-radius: 14px !important;
}

.stTextArea textarea::placeholder {
    color: #587080 !important;
}

.stButton > button {
    width: 100%;
    background-color: #5D8FA8;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #4F7F98;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# OLLAMA SETTINGS
# --------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:1b"


def ask_ai(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code == 200:
            return response.json()["response"].strip()

        return "Sorry, I couldn't respond right now."

    except requests.exceptions.ConnectionError:
        return "Ollama is not running. Please start Ollama first."

    except requests.exceptions.Timeout:
        return "The response took too long. Please try again."

    except Exception:
        return "Something went wrong. Please try again."


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.title("🧘 CalmSpace")

st.markdown(
    "<p style='text-align:center; font-size:18px;'>"
    "Pause. Talk. Reset."
    "</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>"
    "A small space to slow down, understand what you're feeling, "
    "and pause before reacting."
    "</p>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# TALK TO ME
# --------------------------------------------------

st.subheader("💬 Talk to me")

message = st.text_area(
    "What's bothering you?",
    placeholder="Write what happened or what you're feeling...",
    height=150,
    key="talk_message"
)

if st.button("💬 Talk to me", key="talk_button"):

    if message.strip():

        prompt = f"""
You are CalmSpace, a simple emotional support chat assistant.

Your job is to help a person slow down when they are:
angry, frustrated, hurt, disappointed, stressed, confused, or overwhelmed.

Understand the user's actual situation before responding.

Do NOT assume the problem is about:
- exams
- studies
- friends
- relationships
- family
- work

unless the user specifically says so.

Follow this exact structure:

Understanding:
Write 1 short sentence showing that you understood what happened.

Pause:
Write 1 short sentence telling the user not to react impulsively
while they are upset.

Next step:
Give exactly ONE practical action that fits the user's situation.

Question:
Ask exactly ONE simple question that helps understand what the user needs.

STYLE:
- Simple everyday English
- Warm and natural
- Sound like a calm friend
- Situation-specific
- Short and useful
- Do not use dramatic language
- Do not use therapy-style language

NEVER:
- Say "your feelings are valid"
- Say "take a deep breath"
- Suggest breathing exercises
- Suggest meditation
- Suggest grounding
- Suggest body awareness
- Suggest physical exercises
- Use phrases like "emotional energy"
- Use the word "grieve" for normal disappointment
- Give a long list of advice
- Encourage revenge, aggression, insults, or harmful actions
- Claim to be a therapist

If the user gives very little information,
do not make assumptions.
Ask one simple question to understand what happened.

User message:
{message}
"""

        with st.spinner("CalmSpace is listening..."):
            answer = ask_ai(prompt)

        st.info("🧘 CalmSpace")
        st.write(answer)

    else:
        st.warning("Please write something first.")


# --------------------------------------------------
# CALM MY MESSAGE
# --------------------------------------------------

st.divider()

st.subheader("🌿 Calm my message")

st.write(
    "Write the message you feel like sending. "
    "CalmSpace will help make it calmer without removing your main point."
)

angry_message = st.text_area(
    "Your message",
    placeholder="Paste the message you feel like sending...",
    height=150,
    key="angry_message"
)

if st.button("🌿 Make it calmer", key="calm_button"):

    if angry_message.strip():

        prompt = f"""
You are CalmSpace's "Calm my message" feature.

The user has written an emotional or angry message
that they may regret sending.

Rewrite THEIR EXACT MESSAGE into a calmer version.

RULES:
- Keep the original meaning.
- Keep the main complaint.
- Keep the important facts.
- Keep the user's main request.
- Keep the message in first person when appropriate.
- Do not invent facts.
- Do not remove the important issue.
- Remove insults, threats, and aggressive wording.
- Make the message calm, respectful, and natural.
- Keep it reasonably short.
- Do not give advice about the situation.
- Do not explain emotions.
- Do not say "take a deep breath".
- Do not start with "Hello" unless the original starts with a greeting.
- Do not make the message vague.
- Do not replace specific complaints with generic phrases.
- If the original asks for space, keep the request for space.
- If the original asks for an explanation, keep that request.
- If the original identifies a specific problem, keep that problem.

OUTPUT ONLY:

Calmer message:
[rewritten message]

What changed:
[one short sentence]

Original message:
{angry_message}
"""

        with st.spinner("Making your message calmer..."):
            answer = ask_ai(prompt)

        st.success("🌿 Here's a calmer version:")
        st.write(answer)

    else:
        st.warning("Please paste a message first.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "CalmSpace is a supportive reflection tool, not a therapist "
    "or emergency service."
)