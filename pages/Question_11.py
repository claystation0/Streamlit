import streamlit as st
from bson import ObjectId
from pages.tools.utils import *
from streamlit_sortables import sort_items

st.html("""
    <style>
    div[data-testid^="st"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 17px !important;
    }
    </style>
    """)

st.write("### Question 11 of 15")

if "prompt" not in st.session_state:
    st.session_state.prompt = get_random_prompt()

st.write(f"## {st.session_state.prompt}")

if "shuffled_arguments" not in st.session_state:
    st.session_state.stance = st.radio(
        "Please indicate whether you agree with, disagree with, or are neutral about the above prompt.",
        ["Overall agree", "Neutral", "Overall disagree"],
        index=None
    )
    if st.session_state.stance:
        if st.button("Generate arguments"):
            with st.spinner("Generating arguments..."):
                st.session_state.arguments = request_arguments(st.session_state.prompt, st.session_state.stance)
            argument_objects = [
                {"text": st.session_state.arguments[0], "category": "logos"},
                {"text": st.session_state.arguments[1], "category": "ethos"},
                {"text": st.session_state.arguments[2], "category": "pathos"},
                {"text": st.session_state.arguments[3], "category": "all"}
            ]
            st.session_state.shuffled_arguments = randomize(argument_objects, 4)
            st.rerun()
else:
    st.write("**Your stance**: " + st.session_state.stance)
    st.markdown("Please drag and drop the arguments below to arrange them from **most to least** convincing, with the most convincing argument at the top.")
    st.session_state.argument_rankings = sort_items([st.session_state.shuffled_arguments[0]['text'], 
                                                  st.session_state.shuffled_arguments[1]['text'],
                                                  st.session_state.shuffled_arguments[2]['text'],
                                                  st.session_state.shuffled_arguments[3]['text']],
                                                  direction="vertical",
                                                  custom_style=custom_style)
    st.session_state.convincing_score = st.number_input("Given your initial stance, please indicate on the scale the degree to which the arguments have changed your position, if at all. "
                                                        "1 means that your stance has not changed at all as a result of the arguments, 3 means you are ambivalent as to whether they have changed your mind, "
                                                        "and 5 means your stance has definitely changed as a result of the arguments.",
                                                        max_value=5,
                                                        min_value=1,
                                                        step=1)

    if st.session_state.stance and st.session_state.argument_rankings:
        if st.button("Move on to Question 12", type="primary"):
            convincing_score = st.session_state.stance    

            text_to_category = {arg["text"]: arg["category"] for arg in st.session_state.shuffled_arguments}
            rhetoric_rankings = [text_to_category[text] for text in st.session_state.argument_rankings]

            participant_id = st.session_state.get("participant_id")
            if participant_id:
                question_response = {
                    "statement": st.session_state.prompt,
                    "respondent_stance": st.session_state.stance,
                    "llm_stance": st.session_state.llm_stance,
                    "convincing_score": st.session_state.convincing_score,
                    "argument_rankings": rhetoric_rankings,
                    "logos": st.session_state.arguments[0],
                    "ethos": st.session_state.arguments[1],
                    "pathos": st.session_state.arguments[2],
                    "all": st.session_state.arguments[3]
                }

                mongo_client = get_mongo_client()
                collection = get_response_collection()

                collection.update_one(
                    {"_id": ObjectId(participant_id)},
                    {"$push": {"survey_responses": question_response}}
                )

                clear_session_state()
                st.switch_page("pages/Question_12.py")
            else:
                st.warning("No participant ID found. Cannot submit response.")
