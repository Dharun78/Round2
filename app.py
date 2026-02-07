import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Round 2 : AI Bias Detection", page_icon="🕵️")

# 2. Data Calling: Load the CSV
@st.cache_data # This keeps the data in memory so it doesn't reload every click
def load_data():
    try:
        df = pd.read_csv(r'C:\Users\HP\Downloads\New folder\dataset_bias.csv')
        # Convert the Question and Response columns into a searchable dictionary
        return dict(zip(df['Question'], df['Biased_Response']))
    except FileNotFoundError:
        st.error("Error: 'bot2_dataset.csv' not found. Please ensure the file is in the same folder.")
        return {}

bot_responses = load_data()

# 3. Initialize Chat History (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display Sidebar Instructions
with st.sidebar:
    st.title("Round 2 Instructions")
    st.markdown("""Participants must:

-Identify specific biased phrases (not “it’s biased”)

- Classify the bias type:
1.Absolutism
2.Moral superiority
3.Strawman
4.Emotional framing

- Rewrite a neutral, evidence-bounded version
- Personal opinions will not be evaluated. Only analytical identification and correction of bias will be scored.
    """)
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 5. UI Layout
st.title("🤖 Bot 2: Framing Analysis")
st.info("System Status: Active. Framing Mechanism: Enabled.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Logic
if prompt := st.chat_input("Enter your question..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call the data from our dictionary
    # We use .strip() to ignore accidental leading/trailing spaces
    response = bot_responses.get(prompt.strip(), "I'm sorry, that question is not in my verified data bank for Round 2.")

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})