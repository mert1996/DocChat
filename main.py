import streamlit as st
from client.weaviate_client import WeaviateExecuter
from doc_parser import load_docx, chunk_text
from chat_interface import generate_answer

st.set_page_config(page_title="GPT-4 Docx Q&A", layout="centered")
st.title("Word Document QA UI")


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content":  "Hello! You can upload a .docx file and then ask your questions."}
    ]

st.sidebar.header("Upload document")
uploaded_file = st.sidebar.file_uploader("Please upload a .docx file", type=["docx"])
if st.sidebar.button("Create Schema", on_click=WeaviateExecuter().recreate_schema):
    st.sidebar.write("Schema created successfully!")

if uploaded_file is not None:
    with st.spinner("Document is being processed. Please wait..."):
        temp_file_path = "temp_uploaded.docx"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        doc_text = load_docx(temp_file_path)
        chunks = chunk_text(doc_text, chunk_size=500, overlap=120)
        indexed_chunks = list(enumerate(chunks))
        WeaviateExecuter().upload_chunks(indexed_chunks, doc_name=uploaded_file.name)

    st.sidebar.success(f"{uploaded_file.name} file is uploaded and indexed!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Please ask your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    answer = generate_answer(user_input)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)