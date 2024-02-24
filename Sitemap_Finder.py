import streamlit as st
import requests
import re
from bs4 import BeautifulSoup

def sitemap_finder():
    st.title("Sitemap Finder")

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
        # Check in robots.txt
        robots_content = fetch_robots_txt(url)
        if robots_content:
            sitemap_urls = find_sitemap(robots_content)
            for sitemap_url in sitemap_urls:
                if check_sitemap(sitemap_url):
                    return sitemap_url

        # Check common sitemap URLs
        common_sitemap_paths = [
            '/sitemap.xml', '/sitemap_index.xml', '/sitemap1.xml',
            '/sitemap/sitemap-index.xml', '/sitemap_index.xml.gz',
            '/sitemap1.xml.gz', '/sitemap.xml.gz', '/sitemap/sitemap.xml',
            '/sitemap/sitemap1.xml', '/sitemap_index.xml', '/sitemap-index.xml',
            '/sitemap/sitemap_index.xml'
        ]
        for path in common_sitemap_paths:
            common_sitemap_url = url.rstrip("/") + path
            if check_sitemap(common_sitemap_url):
                return common_sitemap_url

        # Parse main page for sitemap links
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

if __name__ == "__main__":
    sitemap_finder()
