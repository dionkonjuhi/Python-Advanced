import streamlit as st

tab1, tab2, tab3 = st.tabs  (["Tab 1", "Tab 2", "Tab 3"])

with tab1:
    st.header("Chelsea i dobt")
    st.write("Content for the first tab")

with tab2:
    st.header("Chelsea i dobt")
    st.write("Content for the second tab")

with tab3:
    st.header("Chelsea i dobt")
    st.write("Content for the third tab")