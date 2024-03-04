import streamlit as st
import json

# Custom CSS to inject for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style/style.css")  # Make sure you have a CSS file at 'style/style.css'

# Initialize session state for dynamic how-to steps
if 'how_to_steps' not in st.session_state:
    st.session_state['how_to_steps'] = [{'name': '', 'url': '', 'image_url': '', 'text': ''}]

# Function to add how-to steps to the session state
def add_step():
    st.session_state['how_to_steps'].append({'name': '', 'url': '', 'image_url': '', 'text': ''})

# Function to remove how-to steps from the session state
def remove_step(index):
    st.session_state['how_to_steps'].pop(index)

# Streamlit layout starts here
st.title("How-to Structured Data Generator")

# Inputs for the main How-to properties
name = st.text_input("Name")
description = st.text_area("Description")
total_time = st.text_input("Total Time")
estimated_cost = st.text_input("Estimated Cost")
currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "INR", "JPY", "Other"])

# Dynamic addition and removal of how-to steps
for idx, step in enumerate(st.session_state['how_to_steps']):
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
        with col1:
            step['text'] = st.text_input(f"Step #{idx+1} Instructions", key=f"text_{idx}")
        with col2:
            step['image_url'] = st.text_input("Image URL", key=f"image_url_{idx}")
        with col3:
            step['name'] = st.text_input("Name", key=f"name_{idx}")
        with col4:
            step['url'] = st.text_input("URL", key=f"url_{idx}")
        with col5:
            st.button("Remove", key=f"remove_{idx}", on_click=remove_step, args=(idx,))

# Button to add new how-to step
st.button("Add Step", on_click=add_step)

# Generate JSON-LD structured data
def generate_json_ld():
    how_to_schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": description,
        "totalTime": total_time,
        "estimatedCost": {
            "@type": "MonetaryAmount",
            "currency": currency,
            "value": estimated_cost
        },
        "step": []
    }
    for step in st.session_state['how_to_steps']:
        if step['text']:
            step_data = {
                "@type": "HowToStep",
                "text": step['text'],
                "url": step['url'],
                "image": step['image_url'],
                "name": step['name']
            }
            how_to_schema["step"].append(step_data)
    return how_to_schema

# Button to generate JSON-LD
if st.button("Generate JSON-LD"):
    json_ld = generate_json_ld()
    st.json(json_ld)  # Displaying the generated JSON-LD in a pretty JSON format

    # Providing a text area for the user to copy the JSON-LD
    st.text_area("Copy the JSON-LD below:", value=json.dumps(json_ld, indent=2), height=300)

# Links to documentation
st.markdown("#### References & Documentation:")
st.markdown("[Schema.org's reference: HowTo](https://schema.org/HowTo)")
st.markdown("[Google's documentation: HowTo](https://developers.google.com/search/docs/advanced/structured-data/how-to)")
