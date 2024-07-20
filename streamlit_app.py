import streamlit as st
import requests
import json
from urllib.parse import urlparse, urlunparse
from urllib.robotparser import RobotFileParser
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def configure_chrome_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/path/to/google-chrome"  # Specify if not standard
    return webdriver.Chrome(ChromeDriverManager(version='specific_version').install(), options=options)

def get_driver():
    options = configure_chrome_options()
    # Use WebDriver Manager to handle driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver
def scrape_google(keyword, locale):
    search_url = f'https://www.google.com/search?q={keyword}&hl={locale}'
    options = configure_chrome_options()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    try:
        driver.get(search_url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        snippet_block = soup.find('div', {'class': 'g'})
        if snippet_block:
            text = snippet_block.get_text(separator=" ", strip=True)
            return text
    finally:
        driver.quit()
    return "No snippet found."

def snippet_scraper():
    st.title("Google Snippet Scraper")
    locales = ['de', 'fr', 'es', 'es-mx', 'it', 'nl', 'da', 'fi', 'sv', 'ja', 'ko', 'pl', 'pt', 'pt-br', 'tr', 'no', 'zh', 'zh-tw', 'zh-hk', 'lt', 'id', 'ar', 'he', 'ru', 'uk']
    keyword = st.text_input("Enter the keyword to search:")
    locale = st.selectbox("Select Locale", locales)
    if st.button("Scrape Snippet"):
        with st.spinner('Scraping...'):
            result = scrape_google(keyword, locale)
            st.text_area("Scraped Snippet", result, height=300)

# from Sitemap_Finder import sitemap_finder  # Assuming you have this from your setup
# Define the sitemap_finder function with all its internal logic
def sitemap_finder():
    st.title("Sitemap Finder")

    # Internal function definitions and logic of sitemap_finder
    def ensure_http_scheme(url):
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        return url

    def fetch_robots_txt(url):
        try:
            full_url = f"{url}/robots.txt"
            response = requests.get(full_url)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            st.error(f"Error fetching robots.txt: {e}")
        return None

    def find_sitemap(robots_content):
        return re.findall(r"Sitemap: (.+)", robots_content, re.IGNORECASE)

    def check_sitemap(url):
        try:
            response = requests.head(url)
            return response.status_code == 200
        except Exception:
            return False

    def find_sitemap_in_html(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a', href=True)
                return [link['href'] for link in links if 'sitemap' in link['href'].lower()]
        except Exception as e:
            st.error(f"Error parsing homepage for sitemap links: {e}")
        return []

    def search_for_sitemaps(url):
        robots_content = fetch_robots_txt(url)
        if robots_content:
            sitemap_urls = find_sitemap(robots_content)
            for sitemap_url in sitemap_urls:
                if check_sitemap(sitemap_url):
                    return sitemap_url

        common_sitemap_paths = [...]
        for path in common_sitemap_paths:
            common_sitemap_url = url.rstrip("/") + path
            if check_sitemap(common_sitemap_url):
                return common_sitemap_url

        sitemap_links = find_sitemap_in_html(url)
        for sitemap_link in sitemap_links:
            if check_sitemap(sitemap_link):
                return sitemap_link

        return None

    user_input = st.text_input("Enter website URL", "")

    if user_input:
        with st.spinner('Searching for sitemaps, please wait...'):
            url = ensure_http_scheme(user_input.strip())
            sitemap_url = search_for_sitemaps(url)
            if sitemap_url:
                st.success(f"Sitemap found: {sitemap_url}")
            else:
                st.error("No accessible Sitemap found using all methods.")

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
    test_url = st.text_input('Enter the URL to test', key="test_url")

    # Dropdown for User-Agent selection with on_change callback
    user_agent = st.selectbox('Select User Agent', ['Googlebot', 'Bingbot', 'DuckDuckBot', 'Googlebot-Image', 'Custom'], key="user_agent")
    if user_agent == 'Custom':
        user_agent = st.text_input('Enter custom User Agent', key="custom_user_agent")

    # Testing and displaying results based on current input values
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
    # About page content here

# FAQ Generator function
def faq_generator():
    st.title("FAQ Page Structured Data Generator")

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

# How-to Structured Data Generator function
def how_to_generator():
    st.title("How-to Structured Data Generator")

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

# CSS & JavaScript Minifier function
def css_js_minifier():
    st.title('CSS & JavaScript Minifier')

    # JavaScript minification section
    st.header('JavaScript Minifier')
    js_code = st.text_area("Enter your JavaScript code here:", height=300)
    minify_js = st.button('Minify JavaScript')

    # CSS minification section
    st.header('CSS Minifier')
    css_code = st.text_area("Enter your CSS code here:", height=300)
    minify_css = st.button('Minify CSS')

    # JavaScript minification logic
    if minify_js and js_code:
        minified_js = jsmin(js_code)
        st.text_area("Minified JavaScript:", minified_js, height=300, key='minified_js')

    # CSS minification logic
    if minify_css and css_code:
        minified_css = compress(css_code)
        st.text_area("Minified CSS:", minified_css, height=300, key='minified_css')

# Main page logic
def email_deliverability_checker():
    st.title('Email Deliverability Checker')

    # Email input area
    emails_input = st.text_area('Type emails here, one per line', height=200)

    # Check Emails button
    if st.button('Check Emails'):
        emails = emails_input.strip().split('\n')
        results = []

        # Progress bar setup
        progress_bar = st.progress(0)
        total_emails = len(emails)

        for index, email in enumerate(emails):
            if email:  # Skip empty lines
                result = is_deliverable(email)
                results.append([email, 'Deliverable' if result else 'Not Deliverable'])
                progress_bar.progress((index + 1) / total_emails)  # Update progress

        # Display results in a DataFrame
        results_df = pd.DataFrame(results, columns=['Email', 'Status'])
        st.dataframe(results_df)

# The rest of your main app logic and other tool functions remain unchanged

# Main page logic with added Email Deliverability Checker
def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Sitemap Finder", "Robots.txt Tester", "FAQ Generator", "How-to Generator", "CSS & JS Minifier", "Email Deliverability Checker", "About"])

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Home", "Snippet Scraper", "Sitemap Finder", "Robots.txt Tester", "FAQ Generator", "How-to Generator", "CSS & JS Minifier", "Email Deliverability Checker", "About"])

    if selection == "Home":
        home_page()
    elif selection == "Snippet Scraper":
        snippet_scraper()
    elif selection == "Sitemap Finder":
        sitemap_finder()
    elif selection == "Robots.txt Tester":
        robots_tester()
    elif selection == "FAQ Generator":
        faq_generator()
    elif selection == "How-to Generator":
        how_to_generator()
    elif selection == "CSS & JS Minifier":
        css_js_minifier()
    elif selection == "Email Deliverability Checker":
        email_deliverability_checker()
    elif selection == "About":
        about_page()
if __name__ == "__main__":
    main()
