from dotenv import dotenv_values
import streamlit as st 

import urllib.request
import json
import ssl
import os

# Function to bypass SSL certificate verification if needed
def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

# Allow self-signed HTTPS certificates (for testing environments)
allowSelfSignedHttps(True)

# Load the API key and endpoint from the .env file
config = dotenv_values(".env")
api_key = config["KEY"]
endpoint = config["ENDPOINT"]

st.title("Diabetes Azure Model Prediction")
st.write("In this project we will sends input data to an Azure model and retrieves predictions.")

st.write("### Enter the data for prediction:")

pregnancies = st.number_input("Pregnancies", min_value=0, step=1)
glucose = st.number_input("Glucose", min_value=0, step=1)
blood_pressure = st.number_input("BloodPressure", min_value=0, step=1)
skin_thickness = st.number_input("SkinThickness", min_value=0, step=1)
insulin = st.number_input("Insulin", min_value=0, step=1)
bmi = st.number_input("BMI", min_value=0.0, step=0.1)
diabetes_pedigree_function = st.number_input("DiabetesPedigreeFunction", min_value=0.0, step=0.01)
age = st.number_input("Age", min_value=0, step=1)

# Button to send data
if st.button("Send Data"):
    if not api_key or not endpoint:
        st.error("API key or endpoint is missing.")
    else:
        # Create the input dictionary
        data_input = {
            "Input": {
                    "Pregnancies": [pregnancies],
                    "Glucose": [glucose],
                    "BloodPressure": [blood_pressure],
                    "SkinThickness": [skin_thickness],
                    "Insulin": [insulin],
                    "BMI": [bmi],
                    "DiabetesPedigreeFunction": [diabetes_pedigree_function],
                    "Age": [age]
                }
            }
        body = str.encode(json.dumps(data_input))

        # Prepare the request body
        body = str.encode(json.dumps(data_input))
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}

        # Send the request to the Azure endpoint
        req = urllib.request.Request(endpoint, body, headers)
        try:
            response = urllib.request.urlopen(req)
            result = response.read().decode("utf-8")
            result_json = json.loads(result)

            outcome = result_json.get("Outcome", [None])[0]

            if outcome == 0:
                st.success("The patient does not have diabetes.")
            elif outcome == 1:
                st.success("The patient has diabetes.")
            else:
                st.warning("Outcome data not available in the response.")
            
        except urllib.error.HTTPError as error:
            st.error(f"The request failed with status code: {error.code}")
            st.write(error.info())
            st.write(error.read().decode("utf8", 'ignore'))
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            