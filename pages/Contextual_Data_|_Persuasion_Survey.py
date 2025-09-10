import streamlit as st
from datetime import datetime, timezone
import random
from pages.tools.utils import *

st.html("""
    <style>
    div[data-testid^="st"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 17px !important;
    }
    </style>
    """)

st.title("Contextual Data")
if 'personalized' not in st.session_state:
    st.session_state.personalized = random.choice([True, False])
st.session_state.gender = st.radio("What is your gender?", 
        ["Male", "Female", "Other"],
        index=None)
st.session_state.age = st.number_input("How old are you?",
                min_value=18,
                max_value=115,
                step=1)
st.session_state.religion = st.radio("If you practice a religion, please select it. If not, please select \"None.\"", 
        ["Christianity", "Islam", "Judaism", "Other", "None"],
        index=None)
st.session_state.stated_values = st.multiselect(
    "Please select your top three values that you most closely align with.", 
    ["Integrity", "Respect", "Justice", "Truth", "Empathy", "Cooperation", "Accountability", "Strength", "Tolerance", "Leadership"],
    max_selections=3)
st.markdown("##### Please complete the [Political Compass Test](https://www.politicalcompass.org/test) to answer the next two questions.")
st.session_state.economic = st.radio("On the political spectrum, do you fall left, right, or center?", 
        ["Right", "Center", "Left"],
        index=None)
st.session_state.authority = st.radio("Are you authoritarian, centrist, or libertarian?", 
        ["Authoritarian", "Centrist", "Libertarian"],
        index=None)
st.session_state.open_minded = st.number_input("On a scale from 1 to 5, how open-minded are you? 5 is extremely open-minded, while 1 is not at all.",
                min_value=1,
                max_value=5,
                step=1)

if st.button("Next", type="primary"):
    required_fields = [
        st.session_state.authority,
        st.session_state.economic,
        st.session_state.stated_values,
        st.session_state.religion,
        st.session_state.gender
    ]
    if not all(required_fields):
        st.warning("Please complete all fields before proceeding.")
    else:
        context = {
            "participant_info": {
                "gender": st.session_state.gender,
                "age": st.session_state.age,
                "religion": st.session_state.religion,
                "economic": st.session_state.economic,
                "authority": st.session_state.authority,
                "top_values": st.session_state.stated_values,
                "perceived_open_mindedness": st.session_state.open_minded
            },
            "personalized": st.session_state.personalized,
            "created_at": datetime.now(timezone.utc)
        }
        collection = get_response_collection()
        result = collection.insert_one(context)
        st.session_state.participant_id = str(result.inserted_id)
        st.switch_page("pages/Question_1.py")
