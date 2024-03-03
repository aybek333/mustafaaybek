import streamlit as st
import requests
from urllib.parse import urlparse, urlunparse
from urllib.robotparser import RobotFileParser

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
        return None

# Streamlit interface
st.title('Robots.txt Tester Tool')

# Input for URL to test
test_url = st.text_input('Enter the URL to test', '')

# Dropdown for User-Agent selection
user_agent = st.selectbox('Select User Agent', ['Googlebot', 'Bingbot', 'DuckDuckBot', 'Googlebot-Image', 'Custom'])
if user_agent == 'Custom':
    user_agent = st.text_input('Enter custom User Agent', '')

# Button to test the URL
if st.button('Test URL'):
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
    else:
        st.error('Please fill out all fields')
