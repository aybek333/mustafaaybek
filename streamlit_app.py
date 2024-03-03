import streamlit as st
import requests
from urllib.parse import urlparse, urlunparse
from urllib.robotparser import RobotFileParser
from Sitemap_Finder import sitemap_finder  # Assuming you have this from your setup

# Function to ensure the URL has a scheme, trying both http and https if necessary
def ensure_url_scheme(url):
    if urlparse(url).scheme in ('http', 'https'):
        return url  # Scheme is already present
    else:
        # Try with http first
        new_url = f"http://{url}"
        if requests.head(new_url).status_code < 400:
            return new_url
        # If http doesn't work, try with https
        new_url = f"https://{url}"
        if requests.head(new_url).status_code < 400:
            return new_url
        # If neither worked, return the original URL and handle the error elsewhere
        return url

# Function to construct the robots.txt URL from the base URL
def construct_robots_txt_url(url):
    url_with_scheme = ensure_url_scheme(url)
    parsed_url = urlparse(url_with_scheme)
    robots_path = urlparse('/robots.txt')
    robots_url = parsed_url._replace(path=robots_path.path, params=robots_path.params, query=robots_path.query, fragment=robots_path.fragment)
    return urlunparse(robots_url)

# Function to fetch and display the robots.txt file
def fetch_and_display_robots_txt(url):
    robots_txt_url = construct_robots_txt_url(url)
    try:
        response = requests.get(robots_txt_url)
        if response.status_code == 200:
            st.text_area("robots.txt contents", response.text, height=300)
            return response.text
        else:
            st.error("Failed to fetch the robots.txt file.")
            return None
    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to check if a URL is allowed by the robots.txt rules
def is_allowed_by_robots(test_url, user_agent, robots_txt_content):
    try:
        rp = RobotFileParser()
        rp.parse(robots_txt_content.splitlines())
        return rp.can_fetch(user_agent, test_url)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Define the Robots.txt Tester Tool as a function
def robots_tester():
    st.title('Robots.txt Tester Tool')

    # Input for URL to test with on_change callback
    test_url = st.text_input('Enter the URL to test', key="test_url", on_change=test_url_changed)

    # Dropdown for User-Agent selection with on_change callback
    user_agent = st.selectbox('Select User Agent', ['Googlebot', 'Bingbot', 'DuckDuckBot', 'Googlebot-Image', 'Custom'], key="user_agent", on_change=user_agent_changed)
    if user_agent == 'Custom':
        user_agent = st.text_input('Enter custom User Agent', key="custom_user_agent", on_change=custom_user_agent_changed)

# Callback functions for handling changes in input fields
def test_url_changed():
    test_and_display_results()

def user_agent_changed():
    test_and_display_results()

def custom_user_agent_changed():
    test_and_display_results()

# Function to handle testing and displaying results based on current input values
def test_and_display_results():
    test_url = st.session_state.get("test_url", "")
    user_agent = st.session_state.get("user_agent", "Custom")
    if user_agent == 'Custom':
        user_agent = st.session_state.get("custom_user_agent", "")

    if test_url and user_agent:
        robots_txt_content = fetch_and_display_robots_txt(test_url)
        if robots_txt_content:
            result = is_allowed_by_robots(test_url, user_agent, robots_txt_content)
            if result is True:
                st.success('Allowed')
            elif result is False:
                st.error('Disallowed')
            else:
                st.warning('Could not determine from the robots.txt file')
# Define other pages as functions
def home_page():
    st.title("Welcome!")
    st.write("I'm Mustafa Aybek, a dedicated SEO Manager with a deep passion for Technical SEO. My journey in the digital marketing landscape has been driven by a relentless pursuit of optimizing website performance, enhancing user experience, and maximizing search engine visibility. With a keen eye for detail and a steadfast commitment to staying ahead of the latest industry trends, I strive to deliver strategies that not only meet but exceed business objectives. Join me as we explore the ever-evolving world of SEO and unlock the full potential of online platforms.")
def about_page():
    st.title("About")
    # About page content...

# Main page logic
def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Sitemap Finder", "Robots.txt Tester", "About"])

    if selection == "Home":
        home_page()
    elif selection == "Sitemap Finder":
        sitemap_finder()  # Call the sitemap_finder function
    elif selection == "Robots.txt Tester":
        robots_tester()  # This now calls the updated robots_tester function
    elif selection == "About":
        about_page()

if __name__ == "__main__":
    main()
