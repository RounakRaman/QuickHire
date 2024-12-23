import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API")

# Streamlit app
def main():
    st.image("https://ibb.co/sK9t45d",width=150)
    st.title("QuickHire: Redefining Off-Campus Hiring")
    
    
    # Input for LinkedIn URL
    linkedin_url = st.text_input("Enter the LinkedIn Profile URL:", placeholder="https://www.linkedin.com/in/example/")
    roles=st.text_input("Enter the roles you are looking for:",placeholder="Example like Data Analyst OR Business Analyst OR Financial Analyst")

    # Button to fetch data
    if st.button("Extract Job Postings"):
        if linkedin_url:
            try:
                headers = {'Authorization': f'Bearer {API_KEY}'}
                api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin/company/job'
                params = {'job_type': 'full-time OR internship',
                            'experience_level':'entry_level',
                            'when':'yesterday',
                            'flexibility': 'anything',
                            'geo_id': '102713980',   #geoID for India
                            'keyword': roles,
                            }
                
                
                # API request
                response = requests.get(api_endpoint, params=params, headers=headers)
                
                # Handle response
                if response.status_code == 200:
                    data = response.json()
                    st.success("Profile data fetched successfully!")
                    st.json(data)  # Display JSON response in a readable format
                else:
                    st.error(f"Failed to fetch data. Status Code: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error("An error occurred while fetching data.")
                st.write(str(e))
        else:
            st.warning("Please enter a valid LinkedIn profile URL.")

if __name__ == "__main__":
    main()