
import streamlit as st

st.title("Instructions")

st.markdown("""
- Please do not refresh at any point during the survey. You will lose your progress if you do.
- You may not return to a question you've passed, so please ensure that the answers you select are final
            before continuing to another question.
- For each question:
  1. Please indicate whether you agree with, disagree with, or feel neutral about the given statement.

  2. Rank the four arguments from most to least convincing.
                
  3. Given your initial stance, please indicate on the scale the degree to which the arguments have changed your position, if at all.
            1 means that your stance has not changed at all as a result of the arguments, 5 means your stance has definitely changed as
            a result of the arguments, and 3 means you are ambivalent as to whether they have changed your mind.
""")

if st.button("Next", type="primary"):
  st.switch_page("pages/Contextual_Data.py")
