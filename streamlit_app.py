import streamlit as st
from reppy.robots import Robots
from reppy.exceptions import ServerError
import requests
from Sitemap_Finder import sitemap_finder  # Make sure to import the sitemap_finder function

# Define the robots tester tool as a function
def robots_tester():
    st.title('Robots.txt Tester Tool')

    # Input for robots.txt URL
    robots_txt_url = st.text_input('Enter the URL of the robots.txt file', '')

    # Input for URL to test
    test_url = st.text_input('Enter the URL to test', '')

    # Dropdown for User-Agent selection
    user_agent = st.selectbox('Select User Agent', ['Googlebot', 'Bingbot', 'DuckDuckBot', 'Googlebot-Image', 'Custom'])
    if user_agent == 'Custom':
        user_agent = st.text_input('Enter custom User Agent', '')

    # Button to test the URL
    if st.button('Test URL'):
        if robots_txt_url and test_url and user_agent:
            robots_txt_content = get_robots_txt(robots_txt_url)
            if robots_txt_content is not None:
                result = is_allowed_by_robots(test_url, user_agent, robots_txt_content)
                if result is True:
                    st.success('Allowed')
                elif result is False:
                    st.error('Disallowed')
                else:
                    st.warning('Could not determine from the robots.txt file')
            else:
                st.error('Could not fetch the robots.txt file')
        else:
            st.error('Please fill out all fields')

# Function to fetch and parse the robots.txt file
def get_robots_txt(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException:
        return None

# Function to check if a URL is allowed by the robots.txt rules
def is_allowed_by_robots(url, user_agent, robots_txt_content):
    try:
        robots = Robots.parse(url, robots_txt_content)
        return robots.allowed(url, user_agent)
    except ServerError as e:
        return None

# Define other pages as functions
def home_page():
    st.title("Welcome!")
    # Home page content...

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
        robots_tester()  # Call the robots_tester function
    elif selection == "About":
        about_page()

if __name__ == "__main__":
    main()
