import streamlit as st
import json

# Custom CSS to inject for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inject custom CSS
local_css("style/style.css")

# Initialize session state for dynamic question-answer pairs
if 'qa_pairs' not in st.session_state:
    st.session_state.qa_pairs = [{'question': '', 'answer': ''}]

# Add question-answer pair to session state
def add_qa_pair():
    st.session_state.qa_pairs.append({'question': '', 'answer': ''})

# Remove question-answer pair from session state
def remove_qa_pair(index):
    st.session_state.qa_pairs.pop(index)

# Streamlit layout
st.title("FAQ Page Structured Data Generator")

# Button to add new question-answer pair
if st.button("Add Question"):
    add_qa_pair()

# Display question-answer pairs
for idx, qa_pair in enumerate(st.session_state.qa_pairs):
    expander = st.expander(f"Q&A #{idx + 1}", expanded=True)
    with expander:
        col1, col2 = st.columns([5, 5])
        with col1:
            qa_pair['question'] = st.text_input(f"Question #{idx+1}", qa_pair['question'], key=f"question_{idx}")
        with col2:
            qa_pair['answer'] = st.text_area("Answer", qa_pair['answer'], key=f"answer_{idx}")
        st.button("Remove", key=f"remove_{idx}", on_click=remove_qa_pair, args=(idx,))

# Generate JSON-LD structured data
def generate_json_ld():
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    for qa_pair in st.session_state.qa_pairs:
        if qa_pair['question'] and qa_pair['answer']:
            faq_schema["mainEntity"].append({
                "@type": "Question",
                "name": qa_pair['question'],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": qa_pair['answer']
                }
            })
    return faq_schema

# Button to generate JSON-LD
if st.button("Generate JSON-LD"):
    json_ld = generate_json_ld()
    st.json(json_ld)

    # Provide a text area for the user to copy the JSON-LD
    st.text_area("Copy the JSON-LD below:", value=json.dumps(json_ld, indent=2), height=250)

# Link to Schema.org and Google's documentation
st.markdown("[Schema.org's reference: FAQPage](https://schema.org/FAQPage)")
st.markdown("[Google's documentation: FAQ Page](https://developers.google.com/search/docs/advanced/structured-data/faqpage)")
