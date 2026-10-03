from numpy import block
import streamlit as st
import requests

st.set_page_config(
    page_title="CalmSpace",
    page_icon="🧘",
    layout="centered"
)
st.markdown("""
<style>

.stApp {
    background-color: #88B5CC;
}

h1 {
    color: #29495C !important;
    text-align: center;
    font-weight: 700;
}

h2, h3 {
    color: #29495C !important;
}

p, label {
    color: #334455 !important;
}

textarea {
    background-color: #C9E2EE !important;
    border: 1px solid #5D8FA8 !important;
    border-radius: 14px !important;
}

.stButton > button {
    background-color: #5D8FA8;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #4F7F98;
}

</style>
""", unsafe_allow_html=True)
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
            return response.json()["response"]

        return "Sorry, I couldn't respond right now."

    except requests.exceptions.ConnectionError:
        return "Ollama is not running. Please start Ollama first."

    except Exception as e:
        return f"Something went wrong: {e}"



st.title("🧘 CalmSpace")
st.subheader("Pause. Talk. Reset.")

st.write(
    "A small space to slow down, understand what you're feeling, "
    "and pause before reacting."
)

message = st.text_area(
    "What's bothering you?",
    placeholder="Write what happened or what you're feeling..."
)

if st.button("💬 Talk to me"):
    if message.strip():

        prompt = f"""
You are CalmSpace.

Your job is to help a person slow down and think clearly when they are
angry, frustrated, stressed, hurt, disappointed, confused, or overwhelmed.

Understand the user's actual situation before responding.
Do not assume the problem is about studies, exams, relationships, or anything else.

Follow this structure:

1. Understanding:
Write 1-2 sentences showing that you understood what happened and why it may be upsetting.

2. Pause:
Give ONE short sentence telling the user not to react impulsively while emotions are high.
Do NOT suggest breathing unless the user specifically asks for it.

3. Next step:
Give ONE practical action that fits the user's actual situation.

4. Question:
Ask ONE useful question that helps move the situation forward.

STYLE:
- Simple English
- Natural and conversational
- Calm and supportive
- Concise
- Situation-specific

NEVER:
- Automatically suggest breathing exercises
- Say "take a deep breath"
- Use exaggerated or dramatic language
- Use therapy-style language
- Give a long list of advice
- Encourage revenge, aggression, insults, or harmful actions
- Do not suggest body awareness, meditation, grounding, or physical exercises.
- Do not ask the user to focus on physical sensations.
- Do not use phrases like "emotional energy" or "raw feelings".

If the user gives very little information, ask one gentle question
instead of making assumptions.

User message:
{message}
"""

        with st.spinner("CalmSpace is listening..."):
            answer = ask_ai(prompt)

        st.info("🧘 CalmSpace")
        st.write(answer)

    else:
        st.warning("Please write something first.")


st.divider()

st.subheader("💬 Calm my message")

angry_message = st.text_area(
    "Want to rewrite an angry message?",
    placeholder="Paste the message you feel like sending..."
)

if st.button("🌿 Make it calmer"):
    if angry_message.strip():

        prompt = f"""
You are CalmSpace's "Calm my message" feature.

The user wrote an emotional or angry message that they may regret sending.

Your job is to rewrite THEIR EXACT MESSAGE into a calmer version.

Rules:
- Keep the original meaning and main concern.
- Keep the message in first person.
- Do not invent new facts.
- Do not remove the important issue.
- Remove insults, blame, threats, and aggressive wording.
- Make it calm, respectful, and natural.
- Keep it short.
- Do not give advice about the situation.
- Do not explain emotions.
- Do not say "take a deep breath".
- Do not start with "Hello" unless the original message starts with a greeting.
- Preserve every important point from the original message.
- Do not remove the main complaint or request.
- Keep the same situation and intent.
- You may soften the wording, but do not make the message vague.
- Do not replace specific complaints with generic phrases like
  "I feel frustrated" or "I am overwhelmed."
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


st.caption(
    "CalmSpace is a supportive reflection tool, not a therapist "
    "or emergency service."
)