# Importing the libraries
import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy as sp
import dabl
import imblearn
import logging

# Setting the OpenAI API key
openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Setting the page config and theme
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Adding a beautiful heading to the page
st.title("Excel file Analyser")

# Creating a file uploader widget on the left side without heading
uploaded_file = st.sidebar.file_uploader("", type="csv")

# Reading and displaying the CSV file
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)

        # Displaying the column names with a text input to change the description on the right of it
        col1, col2 = st.sidebar.columns(2)
        for col in data.columns:
            with col1:
                st.sidebar.write(col)
            with col2:
                new_desc = st.sidebar.text_input("", f"Description of {col}", key=col)
                data = data.rename(columns={col: new_desc})

        # Displaying the check boxes to show the first and last 10 rows without heading
        show_first = st.sidebar.checkbox("Show first 10 rows")
        show_last = st.sidebar.checkbox("Show last 10 rows")
        if show_first:
            st.write(data.head(10))
        if show_last:
            st.write(data.tail(10))

        # Creating a chat bar to prompt the CSV file with OpenAI API on the right side without heading
        col1, col2 = st.columns(2)
        with col2:
            prompt = st.text_input("")
            if prompt:
                response = openai.Completion.create(
                    engine="davinci",
                    prompt=prompt,
                    max_tokens=100,
                    temperature=0.5,
                    stop="\n"
                )
                st.write(response["choices"][0]["text"])

        # Removing null value rows from the data
        data = data.dropna()

        # Performing some data visualization and cleaning tasks using other libraries
        # You can add more code here as per your needs

    except Exception as e:
        logging.error("Error occurred while processing the CSV file", exc_info=e)
        # Writing the error log to a file
        with open("error_log.txt", "a") as f:
            f.write(logging.exception(e))
