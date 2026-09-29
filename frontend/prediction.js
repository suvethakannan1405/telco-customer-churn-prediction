const API_URL = "http://telco-customer-churn-prediction-lfzk.onrender.com";

const predictionForm = document.getElementById("predictionForm");
const predictionError = document.getElementById("predictionError");

const predictionInitial = document.getElementById("predictionInitial");
const predictionResult = document.getElementById("predictionResult");

const predictionText = document.getElementById("predictionText");
const probabilityText = document.getElementById("probabilityText");
const riskText = document.getElementById("riskText");
const predictionMessage = document.getElementById("predictionMessage");
const predictionIcon = document.getElementById("predictionIcon");

const predictButton = document.getElementById("predictButton");
const predictButtonText = document.getElementById("predictButtonText");

const newPredictionButton =
    document.getElementById("newPredictionButton");


// ==========================================
// CHECK LOGIN
// ==========================================

async function checkLogin() {

    try {

        const response = await fetch(
            `${API_URL}/auth-check`,
            {
                method: "GET",
                credentials: "include"
            }
        );

        if (!response.ok) {

            window.location.href = "index.html";

            return false;
        }

        const data = await response.json();

        const username =
            document.getElementById("predictionUsername");

        if (username && data.username) {

            username.textContent = data.username;

        }

        return true;

    } catch (error) {

        console.error("Authentication error:", error);

        return false;
    }
}


// ==========================================
// SHOW ERROR
// ==========================================

function showError(message) {

    predictionError.textContent = message;

    predictionError.classList.remove("hidden");
}


// ==========================================
// HIDE ERROR
// ==========================================

function hideError() {

    predictionError.textContent = "";

    predictionError.classList.add("hidden");
}


// ==========================================
// GET FORM DATA
// ==========================================

function getCustomerData() {

    return {

        gender:
            document.getElementById("gender").value,

        SeniorCitizen:
            document.getElementById("SeniorCitizen").value,

        Partner:
            document.getElementById("Partner").value,

        Dependents:
            document.getElementById("Dependents").value,

        tenure:
            document.getElementById("tenure").value,

        PhoneService:
            document.getElementById("PhoneService").value,

        MultipleLines:
            document.getElementById("MultipleLines").value,

        InternetService:
            document.getElementById("InternetService").value,

        OnlineSecurity:
            document.getElementById("OnlineSecurity").value,

        OnlineBackup:
            document.getElementById("OnlineBackup").value,

        DeviceProtection:
            document.getElementById("DeviceProtection").value,

        TechSupport:
            document.getElementById("TechSupport").value,

        StreamingTV:
            document.getElementById("StreamingTV").value,

        StreamingMovies:
            document.getElementById("StreamingMovies").value,

        Contract:
            document.getElementById("Contract").value,

        PaperlessBilling:
            document.getElementById("PaperlessBilling").value,

        PaymentMethod:
            document.getElementById("PaymentMethod").value,

        MonthlyCharges:
            document.getElementById("MonthlyCharges").value,

        TotalCharges:
            document.getElementById("TotalCharges").value
    };
}


// ==========================================
// PREDICT CUSTOMER
// ==========================================

predictionForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        hideError();

        // Browser validation
        if (!predictionForm.checkValidity()) {

            predictionForm.reportValidity();

            return;
        }


        // Get customer data
        const customerData =
            getCustomerData();


        // Button loading
        predictButton.disabled = true;

        predictButtonText.textContent =
            "⏳ Predicting...";


        try {

            console.log(
                "Sending customer data:",
                customerData
            );


            // Send data to Flask
            const response = await fetch(
                `${API_URL}/predict`,
                {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    credentials: "include",

                    body:
                        JSON.stringify(customerData)
                }
            );


            const data =
                await response.json();


            console.log(
                "Backend response:",
                data
            );


            // Backend error
            if (!response.ok || data.status !== "success") {

                throw new Error(
                    data.message ||
                    "Prediction failed"
                );
            }


            // ======================================
            // DISPLAY RESULT
            // ======================================

            const prediction =
                data.prediction;

            const probability =
                data.churn_probability;

            const risk =
                data.risk_level;


            predictionText.textContent =
                prediction;


            probabilityText.textContent =
                `${probability}%`;


            riskText.textContent =
                risk;


            // ======================================
            // RESULT MESSAGE
            // ======================================

            if (prediction === "CHURN") {

                predictionIcon.textContent = "⚠️";

                predictionMessage.textContent =
                    "This customer has a high likelihood of leaving the telecom service. Consider taking retention actions.";

            } else {

                predictionIcon.textContent = "✅";

                predictionMessage.textContent =
                    "This customer is currently predicted to remain with the telecom service.";

            }


            // ======================================
            // SHOW RESULT
            // ======================================

            predictionInitial.classList.add(
                "hidden"
            );

            predictionResult.classList.remove(
                "hidden"
            );


        } catch (error) {

            console.error(
                "Prediction error:",
                error
            );


            showError(
                "Unable to connect to the prediction backend. Make sure Flask is running on port 5000."
            );


        } finally {

            predictButton.disabled = false;

            predictButtonText.textContent =
                "🔮 Predict Customer Churn";

        }

    }
);


// ==========================================
// NEW PREDICTION
// ==========================================

newPredictionButton.addEventListener(
    "click",
    function () {

        predictionForm.reset();

        predictionResult.classList.add(
            "hidden"
        );

        predictionInitial.classList.remove(
            "hidden"
        );

        hideError();

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }
);


// ==========================================
// PAGE START
// ==========================================

checkLogin();