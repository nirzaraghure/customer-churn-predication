import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load trained model
model = joblib.load("churn_model.pkl")

st.title("🔍 Customer Churn Prediction App")

# Input fields
tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=20.0)
total_charges = st.number_input("Total Charges", min_value=0.0, value=200.0)
senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
gender = st.selectbox("Gender", ["Male", "Female"])
partner = st.selectbox("Partner", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["Yes", "No"])
phone_service = st.selectbox("Phone Service", ["Yes", "No"])
multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
payment_method = st.selectbox("Payment Method", [
    "Electronic check", "Mailed check",
    "Bank transfer (automatic)", "Credit card (automatic)"
])

# Prepare input dictionary
input_dict = {
    'SeniorCitizen': 1 if senior_citizen == "Yes" else 0,
    'tenure': tenure,
    'MonthlyCharges': monthly_charges,
    'TotalCharges': total_charges,
    'gender_Male': 1 if gender == "Male" else 0,
    'Partner_Yes': 1 if partner == "Yes" else 0,
    'Dependents_Yes': 1 if dependents == "Yes" else 0,
    'PhoneService_Yes': 1 if phone_service == "Yes" else 0,
    'MultipleLines_No phone service': 1 if multiple_lines == "No phone service" else 0,
    'MultipleLines_Yes': 1 if multiple_lines == "Yes" else 0,
    'InternetService_Fiber optic': 1 if internet_service == "Fiber optic" else 0,
    'InternetService_No': 1 if internet_service == "No" else 0,
    'OnlineSecurity_No internet service': 1 if online_security == "No internet service" else 0,
    'OnlineSecurity_Yes': 1 if online_security == "Yes" else 0,
    'OnlineBackup_No internet service': 1 if online_backup == "No internet service" else 0,
    'OnlineBackup_Yes': 1 if online_backup == "Yes" else 0,
    'DeviceProtection_No internet service': 1 if device_protection == "No internet service" else 0,
    'DeviceProtection_Yes': 1 if device_protection == "Yes" else 0,
    'TechSupport_No internet service': 1 if tech_support == "No internet service" else 0,
    'TechSupport_Yes': 1 if tech_support == "Yes" else 0,
    'StreamingTV_No internet service': 1 if streaming_tv == "No internet service" else 0,
    'StreamingTV_Yes': 1 if streaming_tv == "Yes" else 0,
    'StreamingMovies_No internet service': 1 if streaming_movies == "No internet service" else 0,
    'StreamingMovies_Yes': 1 if streaming_movies == "Yes" else 0,
    'Contract_One year': 1 if contract == "One year" else 0,
    'Contract_Two year': 1 if contract == "Two year" else 0,
    'PaperlessBilling_Yes': 1 if paperless_billing == "Yes" else 0,
    'PaymentMethod_Credit card (automatic)': 1 if payment_method == "Credit card (automatic)" else 0,
    'PaymentMethod_Electronic check': 1 if payment_method == "Electronic check" else 0,
    'PaymentMethod_Mailed check': 1 if payment_method == "Mailed check" else 0,
}

# Ensure all 30 expected features are present
expected_features = [
    'SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges',
    'gender_Male', 'Partner_Yes', 'Dependents_Yes', 'PhoneService_Yes',
    'MultipleLines_No phone service', 'MultipleLines_Yes',
    'InternetService_Fiber optic', 'InternetService_No',
    'OnlineSecurity_No internet service', 'OnlineSecurity_Yes',
    'OnlineBackup_No internet service', 'OnlineBackup_Yes',
    'DeviceProtection_No internet service', 'DeviceProtection_Yes',
    'TechSupport_No internet service', 'TechSupport_Yes',
    'StreamingTV_No internet service', 'StreamingTV_Yes',
    'StreamingMovies_No internet service', 'StreamingMovies_Yes',
    'Contract_One year', 'Contract_Two year',
    'PaperlessBilling_Yes',
    'PaymentMethod_Credit card (automatic)',
    'PaymentMethod_Electronic check',
    'PaymentMethod_Mailed check'
]

# Fill missing features with 0
for feature in expected_features:
    if feature not in input_dict:
        input_dict[feature] = 0

# Create input DataFrame
input_df = pd.DataFrame([input_dict])

# Predict
if st.button("Predict Churn"):
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]
    if prediction == 1:
        st.error(f"⚠️ Customer is likely to churn. Probability: {probability:.2f}")
    else:
        st.success(f"✅ Customer is not likely to churn. Probability: {probability:.2f}")
