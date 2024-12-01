import streamlit as st
from streamlit_chat import message
from chatbot import chatbot_query

def main():

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask anything 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

    response_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Type your question here...", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = chatbot_query(user_input)['result']
            print("Debug: Chatbot output:", output)  

            if not output:
                output = "I'm sorry, I don't have an answer to that right now."

            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                if i < len(st.session_state['past']):
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state['generated'][i], key=str(i), avatar_style="thumbs")


if __name__ == "__main__":
    main()
