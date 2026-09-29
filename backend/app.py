from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
import os
import sqlite3
import hashlib


# ==========================================
# 1. CREATE FLASK APPLICATION
# ==========================================

app = Flask(__name__)

app.secret_key = "telco-churn-secret-key-2026"

CORS(
    app,
    supports_credentials=True
)


# ==========================================
# 2. DATABASE
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "users.db"
)


def create_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


create_database()


# ==========================================
# 3. PASSWORD HASHING
# ==========================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ==========================================
# 4. LOAD TRAINED MODEL
# ==========================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "best_churn_model.pkl"
)


try:

    model = joblib.load(MODEL_PATH)

    print("==========================================")
    print("TELECOM CUSTOMER CHURN BACKEND")
    print("==========================================")
    print("Model loaded successfully!")
    print("Model path:", MODEL_PATH)

except Exception as e:

    print("==========================================")
    print("ERROR LOADING MODEL")
    print("==========================================")

    print("Error:", str(e))

    model = None


# ==========================================
# 5. HOME ROUTE
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "message":
        "Telecom Customer Churn Prediction API is running",

        "status": "success",

        "model_loaded":
        model is not None

    })


# ==========================================
# 6. REGISTER ROUTE
# ==========================================

@app.route("/register", methods=["POST"])
def register():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "status": "error",

                "message":
                "No registration data received."

            }), 400


        username = data.get(
            "username",
            ""
        ).strip()

        password = data.get(
            "password",
            ""
        )


        # --------------------------------------
        # Validate username
        # --------------------------------------

        if username == "":

            return jsonify({

                "status": "error",

                "message":
                "Username is required."

            }), 400


        if len(username) < 3:

            return jsonify({

                "status": "error",

                "message":
                "Username must contain at least 3 characters."

            }), 400


        # --------------------------------------
        # Validate password
        # --------------------------------------

        if password == "":

            return jsonify({

                "status": "error",

                "message":
                "Password is required."

            }), 400


        if len(password) < 6:

            return jsonify({

                "status": "error",

                "message":
                "Password must contain at least 6 characters."

            }), 400


        # --------------------------------------
        # Hash password
        # --------------------------------------

        password_hash = hash_password(password)


        # --------------------------------------
        # Save user
        # --------------------------------------

        connection = sqlite3.connect(
            DATABASE_PATH
        )

        cursor = connection.cursor()


        try:

            cursor.execute(
                """
                INSERT INTO users
                (username, password)
                VALUES (?, ?)
                """,
                (
                    username,
                    password_hash
                )
            )

            connection.commit()

        except sqlite3.IntegrityError:

            connection.close()

            return jsonify({

                "status": "error",

                "message":
                "Username already exists."

            }), 409


        connection.close()


        return jsonify({

            "status": "success",

            "message":
            "Account created successfully.",

            "username":
            username

        })


    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 400


# ==========================================
# 7. LOGIN ROUTE
# ==========================================

@app.route("/login", methods=["POST"])
def login():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "status": "error",

                "message":
                "No login data received."

            }), 400


        username = data.get(
            "username",
            ""
        ).strip()

        password = data.get(
            "password",
            ""
        )


        password_hash = hash_password(
            password
        )


        connection = sqlite3.connect(
            DATABASE_PATH
        )

        cursor = connection.cursor()


        cursor.execute(
            """
            SELECT username
            FROM users
            WHERE username = ?
            AND password = ?
            """,
            (
                username,
                password_hash
            )
        )


        user = cursor.fetchone()

        connection.close()


        # --------------------------------------
        # Login successful
        # --------------------------------------

        if user:

            session["logged_in"] = True

            session["username"] = username


            return jsonify({

                "status": "success",

                "message":
                "Login successful.",

                "username":
                username

            })


        # --------------------------------------
        # Login failed
        # --------------------------------------

        return jsonify({

            "status": "error",

            "message":
            "Invalid username or password."

        }), 401


    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 400


# ==========================================
# 8. AUTHENTICATION CHECK
# ==========================================

@app.route("/auth-check", methods=["GET"])
def auth_check():

    if session.get("logged_in") is True:

        return jsonify({

            "status": "success",

            "logged_in": True,

            "username":
            session.get("username")

        })


    return jsonify({

        "status": "error",

        "logged_in": False

    }), 401


# ==========================================
# 9. LOGOUT
# ==========================================

@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({

        "status": "success",

        "message":
        "Logged out successfully."

    })


# ==========================================
# 10. PREDICTION ROUTE
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # --------------------------------------
        # Check model
        # --------------------------------------

        if model is None:

            return jsonify({

                "status": "error",

                "message":
                "Trained model could not be loaded."

            }), 500


        # --------------------------------------
        # Get customer data
        # --------------------------------------

        data = request.get_json()


        if not data:

            return jsonify({

                "status": "error",

                "message":
                "No customer data received."

            }), 400


        # --------------------------------------
        # Create dataframe
        # --------------------------------------

        customer = pd.DataFrame({

            "gender": [
                data["gender"]
            ],

            "SeniorCitizen": [
                int(data["SeniorCitizen"])
            ],

            "Partner": [
                data["Partner"]
            ],

            "Dependents": [
                data["Dependents"]
            ],

            "tenure": [
                int(data["tenure"])
            ],

            "PhoneService": [
                data["PhoneService"]
            ],

            "MultipleLines": [
                data["MultipleLines"]
            ],

            "InternetService": [
                data["InternetService"]
            ],

            "OnlineSecurity": [
                data["OnlineSecurity"]
            ],

            "OnlineBackup": [
                data["OnlineBackup"]
            ],

            "DeviceProtection": [
                data["DeviceProtection"]
            ],

            "TechSupport": [
                data["TechSupport"]
            ],

            "StreamingTV": [
                data["StreamingTV"]
            ],

            "StreamingMovies": [
                data["StreamingMovies"]
            ],

            "Contract": [
                data["Contract"]
            ],

            "PaperlessBilling": [
                data["PaperlessBilling"]
            ],

            "PaymentMethod": [
                data["PaymentMethod"]
            ],

            "MonthlyCharges": [
                float(data["MonthlyCharges"])
            ],

            "TotalCharges": [
                float(data["TotalCharges"])
            ]

        })


        # --------------------------------------
        # Prediction
        # --------------------------------------

        prediction = model.predict(
            customer
        )[0]


        probability = model.predict_proba(
            customer
        )[0][1]


        # --------------------------------------
        # Prediction result
        # --------------------------------------

        if int(prediction) == 1:

            prediction_text = "CHURN"

        else:

            prediction_text = "NO CHURN"


        # --------------------------------------
        # Risk level
        # --------------------------------------

        if probability >= 0.70:

            risk = "HIGH"

        elif probability >= 0.40:

            risk = "MEDIUM"

        else:

            risk = "LOW"


        # --------------------------------------
        # Return result
        # --------------------------------------

        return jsonify({

            "status": "success",

            "prediction":
            prediction_text,

            "churn_probability":
            round(
                probability * 100,
                2
            ),

            "risk_level":
            risk

        })


    except KeyError as e:

        return jsonify({

            "status": "error",

            "message":
            f"Missing customer field: {str(e)}"

        }), 400


    except ValueError as e:

        return jsonify({

            "status": "error",

            "message":
            f"Invalid customer value: {str(e)}"

        }), 400


    except Exception as e:

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 400


# ==========================================
# 11. SERVE OUTPUT IMAGES
# ==========================================

@app.route("/outputs/<path:filename>", methods=["GET"])
def serve_outputs(filename):

    outputs_dir = os.path.join(
        BASE_DIR,
        "outputs"
    )

    return send_from_directory(
        outputs_dir,
        filename
    )


# ==========================================
# 12. START SERVER
# ==========================================

if __name__ == "__main__":

    print("==========================================")
    print("Starting Flask Server...")
    print("==========================================")

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
