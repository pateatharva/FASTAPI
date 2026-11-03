
import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/predict"

# Page configuration
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered"
)

# Application title
st.title("🏥 Insurance Premium Category Predictor")
st.markdown("Enter your details below to predict your insurance premium category.")

st.divider()

# Input fields
st.subheader("Personal Information")

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
    "Height (metres)",
    min_value=0.5,
    max_value=2.49,
    value=1.7
)

income_lpa = st.number_input(
    "Annual Income (LPA)",
    min_value=0.1,
    value=10.0
)

smoker = st.selectbox(
    "Are you a smoker?",
    options=[True, False],
    format_func=lambda x: "Yes" if x else "No"
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

st.divider()

# Prediction button
if st.button("🔍 Predict Premium Category", use_container_width=True):

    # Prepare input data
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        with st.spinner("Predicting insurance premium category..."):

            # Send request to FastAPI
            response = requests.post(
                API_URL,
                json=input_data,
                timeout=15
            )

        # Convert API response into JSON
        result = response.json()

        # Check whether request was successful
        if response.status_code == 200:

            # Get prediction from FastAPI response
            prediction = result.get("predicted_category")

            if prediction is not None:
                st.success("Prediction completed successfully!")

                st.subheader("Prediction Result")

                st.success(
                    f"Predicted Insurance Premium Category: {prediction}"
                )

            else:
                st.error("Prediction field not found in API response.")
                st.json(result)

        else:
            st.error(f"API Error: {response.status_code}")
            st.json(result)

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Could not connect to the FastAPI server. "
            "Make sure FastAPI is running."
        )

    except requests.exceptions.Timeout:
        st.error("⏳ Request timed out. Please try again.")

    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")

    except ValueError:
        st.error("The API returned an invalid JSON response.")
