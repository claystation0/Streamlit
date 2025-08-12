import streamlit as st
import pandas as pd
import numpy as np
import random

st.title("Title")

st.header("Debrief")
st.markdown("""
- **Purpose of Research**:
- **Confidentiality and Privacy**:
- ****:
- **Contact Information**: 
""")
consent = st.radio("**Do you consent to taking part in this study and sharing your anonymized information?**", 
                   ["I consent", "I do not consent"],
                   index=None)
if consent == "I consent":
    st.header("Contextual Data")
    st.radio("What is your gender?", 
             ["Male", "Female", "Other"],
             index=None)
    st.slider("How old are you?", 18, 100)
    st.radio("If you practice a religion, please select it. If not, please select \"None.\"", 
             ["Christianity", "Islam", "Judaism", "Other", "None"],
             index=None)
    stated_values = st.multiselect(
        "Please select your top three values that you most closely align with.", 
        ["Community", "Justice", "Religion", "Authenticity", "Imagination", "Integrity"],
        max_selections=3)
    st.markdown(
        "**Please answer to the** [Political Compass Test](https://www.politicalcompass.org/test) **to answer the next two questions.**"
    )
    st.radio("Do you lean left or right?", 
             ["Right", "Left"],
             index=None)
    st.radio("Do you lean authoritarian or libertarian?", 
             ["Authoritarian", "Libertarian"],
             index=None)
    st.select_slider(
        "How open-minded are you?",
        ["Not at all", "Slightly", "Moderately", "Very much so"]
    )

    if st.button("Next", type="primary"):
        st.header("The Survey")
        st.markdown("Please indicate ")
        st.markdown("1. ")
        

