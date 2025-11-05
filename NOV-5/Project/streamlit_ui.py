import os
import streamlit as st
from langchain_agent import create_agent  # Import your ReAct agent builder

# --- Disable LangSmith Tracing Warnings ---
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = "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"

# --- Streamlit Page Setup ---
st.set_page_config(page_title="🏥 Healthcare Appointment Assistant", layout="wide")
st.title("🏥 AI Healthcare Appointment Assistant")
st.caption("Powered by Mistral 7B (via OpenRouter) + FastAPI + LangChain")

st.markdown("""
### 💡 Try prompts like:
- Show me all available doctors  
- What slots are available for dr_1?  
- Book an appointment with dr_2 for Riya Sharma at 3:00 PM  
""")

# --- Initialize session state ---
if "agent" not in st.session_state:
    with st.spinner("Initializing AI agent..."):
        st.session_state.agent = create_agent()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Input area ---
user_input = st.chat_input("Type your question here...")

# --- Handle user input ---
if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    # Get response from agent
    with st.chat_message("assistant"):
        with st.spinner("AI thinking..."):
            try:
                response = st.session_state.agent.invoke({"input": user_input})
                answer = response["output"]
            except Exception as e:
                answer = f"⚠️ Error: {e}"
            st.markdown(answer)
            st.session_state.chat_history.append(("assistant", answer))

# --- Display full chat history ---
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)
