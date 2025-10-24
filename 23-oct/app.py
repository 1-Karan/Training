import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    st.error("Error: OPENROUTER_API_KEY not found in .env file")
    st.stop()

# 2. Streamlit Page Setup
st.set_page_config(page_title="LangChain + OpenRouter Demo", page_icon="💬", layout="centered")
st.markdown("<h1 style='text-align:center;'>LangChain + OpenRouter AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Ask me anything, and I’ll answer using the Mistral model.</p>", unsafe_allow_html=True)
st.write("---")

# 3. User Input
user_query = st.text_area("Enter your question or prompt below:", height=120, placeholder="e.g., Explain how convolutional neural networks work.")
submit = st.button("Submit")

# 4. When user clicks Submit
if submit:
    if not user_query.strip():
        st.warning("Please enter a question or prompt before submitting.")
    else:
        # Initialize model
        llm = ChatOpenAI(
            model="mistralai/mistral-7b-instruct",
            temperature=0.7,
            max_tokens=256,
            api_key=api_key,
            base_url=base_url,
        )

        # Prepare messages
        messages = [
            SystemMessage(content="You are a helpful and concise AI assistant."),
            HumanMessage(content=f"<s>[INST] {user_query} [/INST]"),
        ]

        # Generate response
        with st.spinner("Thinking..."):
            try:
                response = llm.invoke(messages)
                st.success("Response:")
                st.markdown(f"<div style='background-color:#f7f7f7;padding:15px;border-radius:10px;border:1px solid #ddd;'>{response.content.strip()}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
