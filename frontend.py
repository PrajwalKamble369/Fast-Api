import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Insurance Premium Category Predictor")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=119,
    
    value=30
)

weight = st.number_input(
    "Weight (kg)",
    min_value=1.0,
    value=65.0
)

height = st.number_input(
    "Height (m)",
    min_value=0.5,
    max_value=2.5,
    value=1.70
)

income_lpa = st.number_input(
    "Annual Income (LPA)",
    min_value=0.1,
    value=10.0
)

smoker = st.selectbox(
    "Are you a smoker?",
    [True, False]
)

city = st.text_input(
    "City",
    value="Mumbai"
)

occupation = st.selectbox(
    "Occupation",
    [
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job"
    ]
)

if st.button("Predict Premium Category"):

    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(
            API_URL,
            json=payload
        )

        if response.status_code == 200:

            result = response.json()

            st.success(
                f"Predicted Category: {result['predicted_category']}"
            )

            st.json(result)

        else:
            st.error(
                f"Status Code: {response.status_code}"
            )
            st.write(response.text)

    except Exception as e:
        st.error(f"Error: {e}")