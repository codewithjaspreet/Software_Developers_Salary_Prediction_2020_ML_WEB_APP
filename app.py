
import streamlit as st

from predict import show_predict_page
from explore import explore_page

page_Selection = st.sidebar.selectbox("Explore Or Predict" , ("Predict" , "Explore"))

if page_Selection == "Predict":
    show_predict_page()
else:
    explore_page()