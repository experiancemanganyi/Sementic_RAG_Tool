# By E.Manganyi
import streamlit as st
from brain import ask

st.set_page_config(page_title="Semantic RAG", layout="wide")

st.title(" Semantic RAG Tool")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask a question")

if st.button("Send") and user_input:
    answer, sources = ask(user_input)

    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("Bot", answer))
    st.session_state.sources = sources

for role, msg in st.session_state.chat:
    if role == "You":
        st.markdown(f"** User:** {msg}")
    else:
        st.markdown(f"** RAG:** {msg}")

if "sources" in st.session_state:
    st.subheader(" Sources")
    for s in st.session_state.sources:
        st.markdown(f"- **{s['source']}** (page {s['page']})")
        st.write(s["content"][:200] + "...")