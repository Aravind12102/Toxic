import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
import os
import google.generativeai as genai

def get_form_text(form_url):
    try:
        options = Options()

        # Detect chromium and chromedriver paths or fallback to known paths
        chrome_path = shutil.which("chromium") or "/usr/bin/chromium"
        driver_path = shutil.which("chromium-driver") or "/usr/lib/chromium/chromedriver"

        # Debug print (optional)
        print("Chrome path:", chrome_path)
        print("Driver path:", driver_path)

        if not os.path.exists(chrome_path):
            return f"Error: Chrome not found at {chrome_path}"
        if not os.path.exists(driver_path):
            return f"Error: Chromedriver not found at {driver_path}"

        options.binary_location = chrome_path
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(form_url)

        wait = WebDriverWait(driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".o3Dpx")))
        elements_text = [element.text for element in elements]

        driver.quit()
        return elements_text

    except Exception as e:
        return f"Error loading form: {e}"

def get_gemini_response(input_text):
    genai_client = genai.Client(api_key="AIzaSyAfO8S5sipCLNhMgt70HtpFDrpuI7nanfw")
    response = genai_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=input_text
    )
    return response.text

# Streamlit App UI
st.set_page_config(page_title="Google Form AI Assistant", layout="centered")
st.title("📄 Google Form Analyzer with Gemini AI")

form_url = st.text_input("Paste the Google Form URL below:")

if st.button("Analyze Form"):
    if form_url:
        with st.spinner("Loading and analyzing form..."):
            form_content = get_form_text(form_url)

            if isinstance(form_content, str):
                st.error(form_content)
            else:
                gemini_output = get_gemini_response(form_content)

                st.subheader("✅ Extracted Form Text:")
                st.write(form_content)

                st.subheader("💡 Gemini's Analysis:")
                st.write(gemini_output)
    else:
        st.warning("Please enter a valid Google Form URL.")
