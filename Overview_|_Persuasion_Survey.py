import streamlit as st
from streamlit_sortables import sort_items
from pages.tools.utils import custom_style

st.title("The Art of Persuasion: Evaluating the Impact of Ethos, Pathos, and Logos on Argument Effectiveness")

st.markdown("""
- **Student Researcher**: Sabrina Mazumder. For questions or concerns, please contact me at [dylansabrina@gmail.com](mailto:dylansabrina@gmail.com).
- **Purpose of Project**: The goal of the study is to answer these two questions:
  - Between logos, ethos, and pathos, which rhetorical appeal is most effective at changing people’s minds when used by generative artificial intelligence? 
  - Does the persuasive impact of these appeals vary when the arguments built from them are personalized?
- **If You Participate, You Will Be Asked to**: You will be asked to share personal data including gender, age, religion, poltical beliefs, openness,
            personal values, and opinions.
- **Time Required for Participation**: ~15 minutes
- **Risks**: This survey includes exposure to arguments created by generative artificial intelligence that may contain
            bias, emotionally persuasive language, and factual inaccuracies. Some participants may experience discomfort or psychological stress when engaging
            with certain arguments. I will collect limited personal data to contextualize responses. 
            These responses will be stored securely, but as with any online activity, there is the
            risk of a data breach.
- **Benefits**: There are no direct benefits to you. However, you may find the survey questions interesting, 
            and your responses contribute to the growing body of research pertaining to generative artificial intelligence's persuasive capabilities.
- **How Confidentiality Will Be Maintained**: The survey data is anonymized and solely for research purposes. 
            Results will only be reported in aggregate form, ensuring no individual participant will be identified.

By checking the box below, you confirm that you understand the above information and agree to participate in the survey.
""")

consent = st.checkbox("I consent")
if consent:
    if st.button("Next", type="primary"):
        st.switch_page("pages/Instructions.py")
