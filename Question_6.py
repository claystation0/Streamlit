import streamlit as st
from pymongo import MongoClient
from bson import ObjectId
from pages.tools.utils import *

st.title("Question 6 of 15")

st.markdown("""
**Instructions**

1. Please indicate whether you agree with, disagree with, or feel neutral about the below prompt.
            
2. Generate the arguments.

3. Then, rank the four arguments from most to least convincing:
   - Put the most convincing argument letter in the "First" box
   - Put the second most convincing argument letter in the "Second" box  
   - Put the third most convincing argument letter in the "Third" box""")

if "prompt" not in st.session_state:
    st.session_state.prompt = get_random_prompt()

st.write(f"### {st.session_state.prompt}")

st.session_state.stance = st.radio(
    "Please indicate whether you agree with, disagree with, or are neutral about the above prompt.",
    ["Overall agree", "Neutral", "Overall disagree"],
    index=None
)

if "arguments" not in st.session_state:
    if st.button("Generate arguments"):
        st.session_state.arguments = request_arguments(st.session_state.prompt, st.session_state.stance)
        
        argument_objects = [
            {"text": st.session_state.arguments[0], "category": "logos"},
            {"text": st.session_state.arguments[1], "category": "ethos"},
            {"text": st.session_state.arguments[2], "category": "pathos"},
            {"text": st.session_state.arguments[3], "category": "all"}
        ]
        
        st.session_state.shuffled_arguments = randomize(argument_objects, 4)

if "arguments" in st.session_state:
    st.markdown(f"### Arguments")
    st.markdown(
        f"a. {st.session_state.shuffled_arguments[0]['text']}\n"
        f"b. {st.session_state.shuffled_arguments[1]['text']}\n"
        f"c. {st.session_state.shuffled_arguments[2]['text']}\n"
        f"d. {st.session_state.shuffled_arguments[3]['text']}")

    options = ["a", "b", "c", "d"]

    def select_rank(label, exclude_keys):
        remaining_options = [opt for opt in options if opt not in exclude_keys]
        return st.selectbox(label, remaining_options, key=label)

    if "ranking" not in st.session_state:
        st.session_state.ranking = {"first": None, "second": None, "third": None, "fourth": None}

    st.session_state.ranking["first"] = select_rank("First", [])
    st.session_state.ranking["second"] = select_rank("Second", [st.session_state.ranking["first"]])
    st.session_state.ranking["third"] = select_rank(
        "Third",
        [st.session_state.ranking["first"], st.session_state.ranking["second"]]
    )
    st.session_state.ranking["fourth"] = [opt for opt in options if opt not in [
        st.session_state.ranking["first"],
        st.session_state.ranking["second"],
        st.session_state.ranking["third"]
    ]][0]

    if "survey_responses" not in st.session_state:
        st.session_state.survey_responses = []

    if st.button("Question 7", type="primary"):
        keys = ["first", "second", "third", "fourth"]
        if all(st.session_state.ranking.get(k) for k in keys) and st.session_state.stance:
            
            convincing_score = st.session_state.stance
            
            argument_rankings = []
            option_to_index = {"a": 0, "b": 1, "c": 2, "d": 3}
            
            for rank_position in ["first", "second", "third", "fourth"]:
                selected_option = st.session_state.ranking[rank_position]
                argument_index = option_to_index[selected_option]
                category = st.session_state.shuffled_arguments[argument_index]["category"]
                argument_rankings.append(category)
            
            print("Argument rankings:", argument_rankings)

            participant_id = st.session_state.get("participant_id")
            if participant_id:
                question_response = {
                    "convincing_score": st.session_state.stance,
                    "argument_rankings": argument_rankings
                }
                mongo_client = get_mongo_client()
                collection = get_response_collection()

                collection.update_one(
                    {"_id": ObjectId(participant_id)},
                    {"$set": {"survey_responses.6": question_response}}
                )
                st.session_state.pop("prompt")
                st.session_state.pop("arguments")
                st.session_state.pop("shuffled_arguments")
                st.session_state.pop("ranking")
                st.session_state.pop("stance")
                st.switch_page("pages/Question_7.py")
            else:
                st.warning("No participant ID found. Cannot submit response.")
