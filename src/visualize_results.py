import pandas as pd
import os
import joblib

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, auc


# ==========================================
# 1. CREATE OUTPUT FOLDER
# ==========================================

os.makedirs("outputs", exist_ok=True)


# ==========================================
# 2. LOAD DATASET
# ==========================================

df = pd.read_csv(
    "data/telco_churn.csv",
    sep="\t"
)

print("Dataset loaded successfully!")


# ==========================================
# 3. DATA PREPROCESSING
# ==========================================

df = df.drop(
    "customerID",
    axis=1
)

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df["TotalCharges"] = df["TotalCharges"].fillna(
    df["TotalCharges"].median()
)

df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


# ==========================================
# 4. SEPARATE FEATURES AND TARGET
# ==========================================

X = df.drop(
    "Churn",
    axis=1
)

y = df["Churn"]


# ==========================================
# 5. TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# 6. LOAD BEST TRAINED MODEL
# ==========================================

model = joblib.load(
    "models/best_churn_model.pkl"
)

print("Best model loaded successfully!")


# ==========================================
# 7. MAKE PREDICTIONS
# ==========================================

y_pred = model.predict(X_test)

y_probability = model.predict_proba(X_test)[:, 1]

print("Predictions generated successfully!")


# ==========================================
# 8. CONFUSION MATRIX
# ==========================================

cm = confusion_matrix(
    y_test,
    y_pred
)

plt.figure(figsize=(7, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    xticklabels=[
        "No Churn",
        "Churn"
    ],
    yticklabels=[
        "No Churn",
        "Churn"
    ]
)

plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.title(
    "Confusion Matrix - Logistic Regression"
)

plt.tight_layout()

plt.savefig(
    "outputs/confusion_matrix.png",
    dpi=300
)

plt.close()

print("Confusion matrix saved successfully!")


# ==========================================
# 9. ROC CURVE
# ==========================================

fpr, tpr, thresholds = roc_curve(
    y_test,
    y_probability
)

roc_auc = auc(
    fpr,
    tpr
)

plt.figure(figsize=(7, 5))

plt.plot(
    fpr,
    tpr,
    label=f"Logistic Regression (AUC = {roc_auc:.4f})"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title(
    "ROC Curve - Logistic Regression"
)

plt.legend(
    loc="lower right"
)

plt.tight_layout()

plt.savefig(
    "outputs/roc_curve.png",
    dpi=300
)

plt.close()

print("ROC curve saved successfully!")


# ==========================================
# 10. MODEL COMPARISON GRAPH
# ==========================================

results_df = pd.read_csv(
    "outputs/model_comparison.csv"
)

metrics = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1 Score",
    "ROC-AUC"
]

comparison_df = results_df.copy()

for metric in metrics:
    comparison_df[metric] = (
        comparison_df[metric] * 100
    )


plt.figure(figsize=(12, 6))

comparison_df.set_index(
    "Model"
)[metrics].plot(
    kind="bar",
    figsize=(12, 6)
)

plt.xlabel("Machine Learning Model")
plt.ylabel("Score (%)")

plt.title(
    "Machine Learning Model Comparison"
)

plt.xticks(rotation=15)

plt.legend(
    loc="lower right"
)

plt.tight_layout()

plt.savefig(
    "outputs/model_comparison.png",
    dpi=300
)

plt.close()

print("Model comparison graph saved successfully!")


# ==========================================
# 11. FEATURE COEFFICIENTS
# ==========================================

preprocessor = model.named_steps[
    "preprocessor"
]

logistic_model = model.named_steps[
    "model"
]

feature_names = (
    preprocessor
    .get_feature_names_out()
)

coefficients = (
    logistic_model.coef_[0]
)


# ==========================================
# 12. CREATE FEATURE DATAFRAME
# ==========================================

feature_importance = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": coefficients
})

feature_importance["Absolute"] = (
    feature_importance["Coefficient"].abs()
)

feature_importance = (
    feature_importance
    .sort_values(
        "Absolute",
        ascending=False
    )
)


# ==========================================
# 13. TOP 15 FEATURES
# ==========================================

top_features = (
    feature_importance
    .head(15)
    .sort_values(
        "Coefficient"
    )
)


# ==========================================
# 14. FEATURE COEFFICIENT GRAPH
# ==========================================

plt.figure(figsize=(10, 7))

plt.barh(
    top_features["Feature"],
    top_features["Coefficient"]
)

plt.xlabel(
    "Logistic Regression Coefficient"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "Top 15 Features Affecting Customer Churn"
)

plt.tight_layout()

plt.savefig(
    "outputs/feature_coefficients.png",
    dpi=300
)

plt.close()

print("Feature coefficient graph saved successfully!")


# ==========================================
# 15. SAVE FEATURE COEFFICIENTS
# ==========================================

feature_importance.to_csv(
    "outputs/feature_coefficients.csv",
    index=False
)

print("Feature coefficients saved successfully!")


# ==========================================
# 16. FINAL MESSAGE
# ==========================================

print("\n==========================================")
print("VISUALIZATION COMPLETED SUCCESSFULLY!")
print("==========================================")

print("\nFiles created:")

print("1. outputs/confusion_matrix.png")
print("2. outputs/roc_curve.png")
print("3. outputs/model_comparison.png")
print("4. outputs/feature_coefficients.png")
print("5. outputs/feature_coefficients.csv")

print("\n==========================================")
print("STEP 7 COMPLETED!")
print("==========================================")