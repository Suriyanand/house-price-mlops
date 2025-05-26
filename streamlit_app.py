import streamlit as st
import requests

st.title("🏠 House Price Prediction App")

st.subheader("Enter house details below:")

# Input fields
area = st.number_input("Area (in sq ft)", min_value=0)
bedrooms = st.number_input("Number of Bedrooms", min_value=0)
bathrooms = st.number_input("Number of Bathrooms", min_value=0)
stories = st.number_input("Number of Stories", min_value=0)
mainroad = st.selectbox("Main Road Access", ["yes", "no"])
guestroom = st.selectbox("Guest Room", ["yes", "no"])
basement = st.selectbox("Basement", ["yes", "no"])
hotwaterheating = st.selectbox("Hot Water Heating", ["yes", "no"])
airconditioning = st.selectbox("Air Conditioning", ["yes", "no"])
parking = st.number_input("Parking Spaces", min_value=0)
prefarea = st.selectbox("Preferred Area", ["yes", "no"])
furnishingstatus = st.selectbox("Furnishing Status", ["furnished", "semi-furnished", "unfurnished"])

# Submit button
if st.button("Predict Price"):
    # Prepare data
    data = {
        "area": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "stories": stories,
        "mainroad": mainroad,
        "guestroom": guestroom,
        "basement": basement,
        "hotwaterheating": hotwaterheating,
        "airconditioning": airconditioning,
        "parking": parking,
        "prefarea": prefarea,
        "furnishingstatus": furnishingstatus
    }

    try:
        response = requests.post("http://localhost:8000/predict", json=data)
        result = response.json()

        st.success(f"💰 Predicted Price: ₹ {round(result['predicted_price'], 2)}")
    except Exception as e:
        st.error("❌ Failed to get prediction. Is the FastAPI backend running?")
