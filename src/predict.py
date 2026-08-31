import pandas as pd
import joblib


# ==========================================
# 1. LOAD TRAINED MODEL
# ==========================================

model = joblib.load(
    "models/best_churn_model.pkl"
)

print("\n==========================================")
print("TELECOM CUSTOMER CHURN PREDICTION")
print("==========================================")

print("\nModel loaded successfully!")


# ==========================================
# 2. GET CUSTOMER DETAILS
# ==========================================

gender = input("\nGender (Male/Female): ")

senior_citizen = int(
    input("Senior Citizen (0 = No, 1 = Yes): ")
)

partner = input(
    "Partner (Yes/No): "
)

dependents = input(
    "Dependents (Yes/No): "
)

tenure = int(
    input("Tenure (months): ")
)

phone_service = input(
    "Phone Service (Yes/No): "
)

multiple_lines = input(
    "Multiple Lines (Yes/No/No phone service): "
)

internet_service = input(
    "Internet Service (DSL/Fiber optic/No): "
)

online_security = input(
    "Online Security (Yes/No/No internet service): "
)

online_backup = input(
    "Online Backup (Yes/No/No internet service): "
)

device_protection = input(
    "Device Protection (Yes/No/No internet service): "
)

tech_support = input(
    "Tech Support (Yes/No/No internet service): "
)

streaming_tv = input(
    "Streaming TV (Yes/No/No internet service): "
)

streaming_movies = input(
    "Streaming Movies (Yes/No/No internet service): "
)

contract = input(
    "Contract (Month-to-month/One year/Two year): "
)

paperless_billing = input(
    "Paperless Billing (Yes/No): "
)

payment_method = input(
    "Payment Method: "
)

monthly_charges = float(
    input("Monthly Charges: ")
)

total_charges = float(
    input("Total Charges: ")
)


# ==========================================
# 3. CREATE CUSTOMER DATAFRAME
# ==========================================

customer = pd.DataFrame({

    "gender": [gender],

    "SeniorCitizen": [senior_citizen],

    "Partner": [partner],

    "Dependents": [dependents],

    "tenure": [tenure],

    "PhoneService": [phone_service],

    "MultipleLines": [multiple_lines],

    "InternetService": [internet_service],

    "OnlineSecurity": [online_security],

    "OnlineBackup": [online_backup],

    "DeviceProtection": [device_protection],

    "TechSupport": [tech_support],

    "StreamingTV": [streaming_tv],

    "StreamingMovies": [streaming_movies],

    "Contract": [contract],

    "PaperlessBilling": [paperless_billing],

    "PaymentMethod": [payment_method],

    "MonthlyCharges": [monthly_charges],

    "TotalCharges": [total_charges]
})


# ==========================================
# 4. MAKE PREDICTION
# ==========================================

prediction = model.predict(
    customer
)

probability = model.predict_proba(
    customer
)[0][1]


# ==========================================
# 5. DISPLAY RESULT
# ==========================================

print("\n==========================================")
print("PREDICTION RESULT")
print("==========================================")


if prediction[0] == 1:

    print("\nPrediction: CHURN")

else:

    print("\nPrediction: NO CHURN")


# ==========================================
# 6. CHURN PROBABILITY
# ==========================================

print(
    f"Churn Probability: {probability * 100:.2f}%"
)


# ==========================================
# 7. RISK LEVEL
# ==========================================

if probability >= 0.70:

    risk = "HIGH"

elif probability >= 0.40:

    risk = "MEDIUM"

else:

    risk = "LOW"


print(
    "Risk Level:",
    risk
)


print("\n==========================================")
print("PREDICTION COMPLETED")
print("==========================================")