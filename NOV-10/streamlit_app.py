import streamlit as st
import requests

st.set_page_config(page_title="FastAPI + Streamlit Demo", page_icon="🤝", layout="centered")

BACKEND = "http://127.0.0.1:8000"
st.title("FastAPI + Streamlit 🤝")

with st.expander("🧮 Add Two Numbers (Math)"):
    a = st.number_input("a", value=45.0)
    b = st.number_input("b", value=35.0)
    if st.button("Add"):
        try:
            r = requests.post(f"{BACKEND}/api/add", json={"a": a, "b": b}, timeout=15)
            st.success(f"Answer: {r.json()['sum']}")
        except Exception as e:
            st.error(f"Error: {e}")

with st.expander("📅 Today's Date (IST)"):
    if st.button("Get date/time"):
        try:
            r = requests.get(f"{BACKEND}/api/date", timeout=15).json()
            st.info(f"Today (IST): {r['today_ist']} • Time: {r['time_ist']}")
        except Exception as e:
            st.error(f"Error: {e}")

with st.expander("🔁 Reverse this Word: '_____'"):
    word = st.text_input("Word", value="")
    if st.button("Reverse"):
        try:
            r = requests.post(f"{BACKEND}/api/reverse", json={"text": word}, timeout=15)
            st.success(f"Reversed: {r.json()['reversed']}")
        except Exception as e:
            st.error(f"Error: {e}")

st.subheader("🧠 Ask the Model (FastAPI → OpenRouter)")
query = st.text_area("Your question", placeholder="Tell me today's date - query")
if st.button("Submit"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        try:
            r = requests.post(f"{BACKEND}/api/generate", json={"query": query}, timeout=60)
            if r.ok:
                st.write(f"**Answer:**\n\n{r.json()['response']}")
            else:
                st.error(f"Error {r.status_code}: {r.text}")
        except Exception as e:
            st.error(f"Error: {e}")

