import streamlit as st
from router_chain import function_router

st.set_page_config(page_title="Otipy AI Reporting", )
st.title("Otipy chat bot")

# openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What is this data about?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        print("--------------------------------------", st.session_state.messages[-1]['content'])
        response = function_router(7986640195).router(st.session_state.messages[-1]['content'])
        print(type(response))
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
