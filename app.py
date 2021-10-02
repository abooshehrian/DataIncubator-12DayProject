import streamlit as st

st.title('Hello world')

with st.echo():
    x = 15

with st.echo():
    y = 50

with st.echo():
    z = x + y
    st.write(z)
