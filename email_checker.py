# First, ensure dnspython is installed in your environment:
# pip install dnspython

import streamlit as st
import smtplib
import dns.resolver
import pandas as pd

# Function to check email deliverability
def is_deliverable(email):
    try:
        domain = email.split('@')[1]
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)
        server = smtplib.SMTP()
        server.set_debuglevel(0)  # Set to 1 for verbose output
        server.connect(mx_record)
        server.helo(server.local_hostname)  # Identify ourselves with the remote SMTP server
        server.mail('me@example.com')
        code, message = server.rcpt(str(email))
        server.quit()
        return code == 250
    except:
        return False

# Streamlit UI
def main():
    st.title('Email Deliverability Checker')

    # Text area for user input
    emails_input = st.text_area('Type emails here, one per line', height=200)

    # Button to check emails
    if st.button('Check Emails'):
        emails = emails_input.strip().split('\n')
        results = []

        # Progress bar setup
        progress_bar = st.progress(0)
        total_emails = len(emails)

        for index, email in enumerate(emails, start=1):
            if email:  # Skip empty lines
                result = is_deliverable(email)
                results.append([email, 'Deliverable' if result else 'Not Deliverable'])
                progress_bar.progress(index / total_emails)  # Update progress

        # Display results in a DataFrame
        results_df = pd.DataFrame(results, columns=['Email', 'Status'])
        st.dataframe(results_df)

if __name__ == "__main__":
    main()
