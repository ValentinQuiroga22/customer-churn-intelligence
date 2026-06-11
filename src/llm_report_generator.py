import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_llm_report(prompt):

    return "DEPLOY TEST OK"
