import streamlit as st
from Sitemap_Finder import sitemap_finder  # Make sure to import the sitemap_finder function

# Define other pages as functions
def home_page():
    st.title("Welcome!")
    st.write("I'm Mustafa Aybek, a dedicated SEO Manager with a deep passion for Technical SEO. My journey in the digital marketing landscape has been driven by a relentless pursuit of optimizing website performance, enhancing user experience, and maximizing search engine visibility. With a keen eye for detail and a steadfast commitment to staying ahead of the latest industry trends, I strive to deliver strategies that not only meet but exceed business objectives. Join me as we explore the ever-evolving world of SEO and unlock the full potential of online platforms.")

def about_page():
    st.title("About")
    st.write("Information about this tool.")

# Main page logic
def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Sitemap Finder", "About"])

    if selection == "Home":
        home_page()
    elif selection == "Sitemap Finder":
        sitemap_finder()  # Call the sitemap_finder function
    elif selection == "About":
        about_page()

if __name__ == "__main__":
    main()
