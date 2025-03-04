import streamlit as st
from openai import OpenAI
from streamlit_js_eval import streamlit_js_eval

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-image: url('https://source.unsplash.com/1600x900/?technology,office');
        background-size: cover;
        background-attachment: fixed;
    }
    .main-title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #ff9800;
    }
    .info-box {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 15px;
        border-radius: 10px;
    }
    .chat-box {
        background-color: rgba(240, 240, 240, 0.9);
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit page configuration
st.set_page_config(page_title="Interview Practice App", page_icon="🎤", layout="centered")

st.markdown("<div class='main-title'>Interview Practice App 🎤</div>", unsafe_allow_html=True)

# Initialize session state variables
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0
if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# Setup Function
def complete_setup():
    st.session_state.setup_complete = True

def show_feedback():
    st.session_state.feedback_shown = True

# Collect User Details
if not st.session_state.setup_complete:
    st.markdown("<div class='sub-header'>Personal Information 📝</div>", unsafe_allow_html=True)

    st.session_state["name"] = st.text_input("Name", placeholder="Enter your name", max_chars=40)
    st.session_state["experience"] = st.text_area("Experience", placeholder="Describe your experience", max_chars=200)
    st.session_state["skills"] = st.text_area("Skills", placeholder="List your skills", max_chars=200)

    # Company and Position Selection
    st.markdown("<div class='sub-header'>Company & Position 💼</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state["level"] = st.radio("Experience Level", ["Junior", "Mid-level", "Senior"], index=0)
    with col2:
        st.session_state["position"] = st.selectbox("Position", ["Data Scientist", "Data Engineer", "ML Engineer", "BI Analyst", "Financial Analyst"])

    st.session_state["company"] = st.selectbox("Company", ["Amazon", "Meta", "Google", "Chase", "Microsoft", "LinkedIn", "Spotify"])

    if st.button("Start Interview 🚀", on_click=complete_setup):
        st.success("Setup complete. Starting interview...")

# Interview Chat
if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:
    st.markdown("<div class='sub-header'>Interview Session 🎙️</div>", unsafe_allow_html=True)
    
    st.info("Start by introducing yourself", icon="👋")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"
    
    if not st.session_state.messages:
        st.session_state.messages = [{
            "role": "system",
            "content": (f"You are an HR executive interviewing {st.session_state['name']} "
                        f"for the {st.session_state['level']} {st.session_state['position']} "
                        f"position at {st.session_state['company']}. "
                        "Conduct the interview professionally.")
        }]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if st.session_state.user_message_count < 5:
        if prompt := st.chat_input("Your response", max_chars=1000):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            if st.session_state.user_message_count < 4:
                with st.chat_message("assistant"):
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=st.session_state.messages,
                        stream=True,
                    )
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})

            st.session_state.user_message_count += 1
    
    if st.session_state.user_message_count >= 5:
        st.session_state.chat_complete = True

# Feedback Section
if st.session_state.chat_complete and not st.session_state.feedback_shown:
    if st.button("Get Feedback 🏆", on_click=show_feedback):
        st.write("Fetching feedback...")

if st.session_state.feedback_shown:
    st.markdown("<div class='sub-header'>Interview Feedback 📝</div>", unsafe_allow_html=True)
    
    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])

    feedback_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    feedback_completion = feedback_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Evaluate the interview and provide feedback."},
                  {"role": "user", "content": conversation_history}]
    )
    st.write(feedback_completion.choices[0].message.content)
    
    if st.button("Restart Interview 🔄", type="primary"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
