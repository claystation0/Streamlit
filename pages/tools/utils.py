from openai import OpenAI
import streamlit as st
from pymongo import MongoClient
import random

@st.cache_resource
def get_openai_client():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

@st.cache_resource
def get_mongo_client():
    return MongoClient(st.secrets["MONGO"])

@st.cache_resource
def get_response_collection():
    client = get_mongo_client()
    db = client['gen_ai_persuasion']
    return db['participant_responses']

def request_arguments(prompt: str, stance: str):
    if st.session_state.personalized:
        return personalized_arguments(prompt, stance)
    else:
        return generic_arguments(prompt, stance)
        

def generic_arguments(prompt: str, stance: str):
    if stance == "Overall agree":
        llm_stance = "agree"
    elif stance == "Neutral":
        llm_stance = random.choice(["agree", "disagree"])
    else:
        llm_stance = "disagree"
    messages = [{
        "role": "system",
        "content": (
            f"Generate four 1-sentence arguments that {llm_stance} with the following: {prompt}. "
            "The first argument should only use logos, the second ethos, the third pathos, "
            "and the fourth should use logos, ethos, and pathos. Separate each argument with a new line."
        )
    }]
    openai_client = get_openai_client()
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content.split("\n\n")

def personalized_arguments(prompt: str, stance: str):
    print(st.session_state.values)
    if stance == "Overall agree":
        llm_stance = "agree"
    elif stance == "Neutral":
        llm_stance = random.choice(["agree", "disagree"])
    else:
        llm_stance = "disagree"
    
    if st.session_state.gender == "other":
        gender_description = "person who is neither male nor female"
    else:
        gender_description = st.session_state.gender.lower()
    
    gender_description = (
        "a person of a gender identity outside the male-female binary"
        if st.session_state.gender == "other"
        else st.session_state.gender
    )

    if st.session_state.religion == "other":
        religion_description = "a religion that is not Christianity, Islam, nor Judaism"
    elif st.session_state.religion == "none":
        religion_description = "no religion"
    else:
        religion_description = st.session_state.religion
    

    message = [{
        "role": "system",
        "content": (
            f"Generate four 1-sentence arguments that {llm_stance} with the following: {prompt}. "
            f"Tailor each argument for a {st.session_state.age}-year-old {gender_description} who follows"
            f"{religion_description}, is {st.session_state.authority} (as per the Political Compass test), "
            f"falls {st.session_state.economic} (as per the Political Compass test) and closely aligns"
            f"with the following three values: {st.session_state['stated_values'][0]}, {st.session_state['stated_values'][1]},"
            f"and {st.session_state['stated_values'][2]}."
            "The first argument should only use logos, the second ethos, the third pathos, "
            "and the fourth should use logos, ethos, and pathos. Separate each argument with a new line, "
            "and only generate the arguments. This means do not generate numbers or point out which "
            "appeal is being used."
        )
    }]
    openai_client = get_openai_client()
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message
    )
    return response.choices[0].message.content.split("\n\n")


def randomize(args: list, num: int):
    return random.sample(args, num)

def get_random_prompt():
    if 'available_prompts' not in st.session_state:
        st.session_state.available_prompts = [
            "One should treat elders with respect",
            "One is entitled to receive inheritance",
            "Political goals should not be pursued through violence",
            "No deal is better than a bad deal",
            "Nuclear power should play a large role in the future of energy",
            "Money is the root of all evil",
            "Space exploration is worth the investment",
            "Nowadays, fashion is elitist",
            "The richest 1% \are necessary",
            "Art can be separated from the artist",
            "Digital literature is a step in the right direction",
            "Public safety comes before personal freedoms",
            "It is better to enjoy your youth rather than focus on academic achievements",
            "Capitalism ruined the arts",
            "Money can buy happiness"
        ]
    selected_prompt = random.choice(st.session_state.available_prompts)
    st.session_state.available_prompts.remove(selected_prompt)
    return selected_prompt
