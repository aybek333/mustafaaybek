# Import necessary libraries
import streamlit as st
from jsmin import jsmin
from csscompressor import compress

# Set up the Streamlit interface
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
