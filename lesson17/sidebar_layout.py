import streamlit as st

st.sidebar.header("Sidebar")

st.sidebar.write("This is the sidebar")

st.sidebar.selectbox("Chose an option" , ["Oprion 1","Option 2","Oprion 3"])
st.header.radio("Go to",["Home","Data", "Settings"])