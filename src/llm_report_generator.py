import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

# ==========================================
# LOAD MODEL
# ==========================================

model = genai.GenerativeModel("gemini-1.5-flash")

# ==========================================
# GENERATE REPORT
# ==========================================


def generate_llm_report(prompt):

    try:
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"ERROR: {str(e)}"
