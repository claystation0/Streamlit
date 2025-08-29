import streamlit as st

st.title("Persuasion Survey: Overview")

st.markdown("""
- Student Researcher: Sabrina Mazumder
- Title of Project: The Art of Persuasion: Evaluating theImpact of Ethos, Pathos, and Logos on Argument Effectiveness
- Purpose of Project: The goal of the study is to determine which types of arguments are most convincing.
- If You Participate, You Will Be Asked to: You will be asked to share personal data including gender, age, religion, poltical beliefs, openness,
            personal values, and opinions.
- Time Required for Participation: ~25 minutes
- Risks: This survey includes exposure to arguments created by generative artificial intelligence that may contain
            bias, emotionally persuasive language, and factual inaccuracies. I will collect limited personal data to
            contextualize responses. These responses will be stored securely, but as with any online activity, there is the
            risk of a data breach. Some participants may experience discomfort or psychological stress when engaging
            with certain arguments.
- Benefits: There are no direct benefits to you.
- How Confidentiality Will Be Maintained: The survey is anonymized and asks for no personally identifiable information.
            Only the primary researcher will have access to the raw dataset. Results will only be reported in aggregate form,
            ensuring no individual participant will be identified.
By checking the box below, you confirm that you understand the information provided and agree to participate in the survey.
""")
consent = st.checkbox("I consent")
if consent:
    if st.button("Next", type="primary"):
        st.switch_page("pages/Contextual_Data_|_Persuasion_Survey.py")
