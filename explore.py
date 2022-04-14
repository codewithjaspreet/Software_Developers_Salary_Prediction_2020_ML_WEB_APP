from cProfile import label
from functools import cache
from itertools import groupby
from typing import AsyncGenerator
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
def simplify(categories, cutoff):
    ans = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            ans[categories.index[i]] = categories.index[i]
        else:
            ans[categories.index[i]] = 'Other'
    return ans


def exp(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def edu(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = simplify(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(exp)
    df["EdLevel"] = df["EdLevel"].apply(edu)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def explore_page():

    st.title("Explore Software Engineer Salaries")

    st.write(""" 
        ### Stack Overflow Developer Survey 2020
    """)
    data = df["Country"].value_counts()

    fig1 , ax1 = plt.subplots()
    ax1.pie(data , labels = data.index , autopct= "%1.1f%%" ,shadow=True,startangle = 90)
    ax1.axis("equal")

    st.write("""
        #### Number of Data from different Countries
     """)

    st.pyplot(fig1)

    
    st.write("""
        #### Mean Salary Based on Country
     """)

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
