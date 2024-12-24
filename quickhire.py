import streamlit as st
import json
from linkedin_api import Linkedin
import datetime

# Title of the app
st.image("https://i.ibb.co/K2xmgNp/Beyond-Tech-Logo-page-0001.jpg", width=150)
st.title("QuickHire: Redefining Off-Campus Hiring")

# Instructions in a pop-up modal
if "show_instructions" not in st.session_state:
    st.session_state.show_instructions = True

if st.session_state.show_instructions:
    st.info("""
    Welcome to QuickHire!
    
    This app allows you to search for the latest off-campus job postings through recent posts from LinkedIn. Please enter your LinkedIn username and password to authenticate.
    
    **Instructions:**
    - Make sure your secondary LinkedIn credentials are valid and don't have 2-Factor Authentication.
    - The app fetches recent job posts with keywords like "hire" or "hiring".
    - The results include job titles, links, company names, locations, and posting times.
    """, icon="ℹ️")
    if st.button("Got it"):
        st.session_state.show_instructions = False

# Form for LinkedIn credentials
with st.form("login_form"):
    username = st.text_input("LinkedIn Username", value="", placeholder="Enter your LinkedIn username")
    password = st.text_input("LinkedIn Password", value="", type="password", placeholder="Enter your LinkedIn password")
    submit = st.form_submit_button("Submit")

if submit:
    if username and password:
        try:
            # Authenticate with LinkedIn using username and password
            linkedin = Linkedin(username, password)
            st.success("Logged in successfully!")

            # Search job posts
            st.write("Fetching job postings...")
            posts = linkedin.search(
                params={"keywords": '"hire"+OR+"hiring"'},
                limit=10
            )

            if posts:
                st.write("### Latest Job Posts")
                for response in posts:
                    title = response.get('title', {}).get('text', 'N/A') if response.get('title') else 'N/A'
                    company_name = response.get('primarySubtitle', {}).get('text', 'N/A') if response.get('primarySubtitle') else 'N/A'
                    location = response.get('secondarySubtitle', {}).get('text', 'N/A') if response.get('secondarySubtitle') else 'N/A'
                    job_link = response.get('navigationUrl', 'N/A') or 'N/A'

                    st.write(f"**Job Title:** {title}")
                    st.write(f"**Company Name:** {company_name}")
                    st.write(f"**Location:** {location}")
                    st.write(f"[Job Link]({job_link})")

                    # Extract posting time
                    insights = response.get('insightsResolutionResults', [])
                    if insights:
                        footer = insights[0].get('jobPostingFooterInsight', {}).get('footerItems', [])
                        if footer and footer[0].get('type') == 'LISTED_DATE':
                            timestamp = footer[0].get('timeAt')
                            if timestamp:
                                posted_date = datetime.datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
                                st.write(f"**Posted Date:** {posted_date}")
                            else:
                                st.write("**Posted Date:** Not available.")
                        else:
                            st.write("**Posted Date:** Not available.")
                    else:
                        st.write("**Posted Date:** Not available.")
                    st.write("---")
            else:
                st.write("No job postings found.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter both username and password.")
