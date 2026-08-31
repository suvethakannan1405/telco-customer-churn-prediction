import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/telco_churn.csv", sep="\t")

print("Original Dataset Shape:")
print(df.shape)


# ==========================================
# 2. REMOVE CUSTOMER ID
# ==========================================

df = df.drop("customerID", axis=1)

print("\nAfter removing customerID:")
print(df.shape)


# ==========================================
# 3. CONVERT TOTALCHARGES TO NUMERIC
# ==========================================

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)


# ==========================================
# 4. CHECK MISSING VALUES
# ==========================================

print("\nMissing values:")
print(df.isnull().sum())


# ==========================================
# 5. HANDLE MISSING VALUES
# ==========================================

df["TotalCharges"] = df["TotalCharges"].fillna(
    df["TotalCharges"].median()
)

print("\nMissing values after handling:")
print(df.isnull().sum())


# ==========================================
# 6. CONVERT CHURN TO NUMERIC
# ==========================================

df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


# ==========================================
# 7. SEPARATE FEATURES AND TARGET
# ==========================================

X = df.drop("Churn", axis=1)

y = df["Churn"]


# ==========================================
# 8. DISPLAY FEATURES
# ==========================================

print("\nFeatures (X):")
print(X.columns.tolist())


print("\nTarget (y):")
print(y.value_counts())


# ==========================================
# 9. IDENTIFY NUMERICAL FEATURES
# ==========================================

numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns


# ==========================================
# 10. IDENTIFY CATEGORICAL FEATURES
# ==========================================

categorical_features = X.select_dtypes(
    include=["object"]
).columns


print("\nNumerical Features:")
print(numerical_features.tolist())


print("\nCategorical Features:")
print(categorical_features.tolist())


# ==========================================
# 11. TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\n==========================================")
print("TRAIN TEST SPLIT")
print("==========================================")

print("Training data:")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)

print("\nTesting data:")
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)


# ==========================================
# 12. PREPROCESSING
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            StandardScaler(),
            numerical_features
        ),
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)


print("\n==========================================")
print("PREPROCESSING SETUP")
print("==========================================")

print("Numerical features will be scaled.")
print("Categorical features will be One-Hot Encoded.")


# ==========================================
# 13. DEFINE MACHINE LEARNING MODELS
# ==========================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        random_state=42
    )
}


# ==========================================
# 14. TRAIN MACHINE LEARNING MODELS
# ==========================================

trained_models = {}


print("\n==========================================")
print("MODEL TRAINING")
print("==========================================")


for name, model in models.items():

    print("\nTraining:", name)

    # Create pipeline
    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    # Train model
    pipeline.fit(
        X_train,
        y_train
    )

    # Store trained model
    trained_models[name] = pipeline

    print(name, "trained successfully!")


# ==========================================
# 15. TRAINING COMPLETED
# ==========================================

print("\n==========================================")
print("ALL MODELS TRAINED SUCCESSFULLY!")
print("==========================================")

print("\nModels trained:")

for name in trained_models:
    print("-", name)


# ==========================================
# 16. MODEL EVALUATION
# ==========================================

print("\n==========================================")
print("MODEL EVALUATION")
print("==========================================")


results = []


for name, pipeline in trained_models.items():

    print("\n------------------------------------------")
    print("Evaluating:", name)
    print("------------------------------------------")


    # ======================================
    # MAKE PREDICTIONS
    # ======================================

    y_pred = pipeline.predict(X_test)


    # ======================================
    # PREDICTION PROBABILITY
    # ======================================

    y_probability = pipeline.predict_proba(X_test)[:, 1]


    # ======================================
    # CALCULATE METRICS
    # ======================================

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        y_probability
    )


    # ======================================
    # DISPLAY METRICS
    # ======================================

    print("\nAccuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))
    print("ROC-AUC  :", round(roc_auc, 4))


    # ======================================
    # CONFUSION MATRIX
    # ======================================

    print("\nConfusion Matrix:")

    cm = confusion_matrix(
        y_test,
        y_pred
    )

    print(cm)


    # ======================================
    # CLASSIFICATION REPORT
    # ======================================

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "No Churn",
                "Churn"
            ],
            zero_division=0
        )
    )


    # ======================================
    # STORE RESULTS
    # ======================================

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc
    })


# ==========================================
# 17. CREATE MODEL COMPARISON TABLE
# ==========================================

results_df = pd.DataFrame(results)


print("\n==========================================")
print("MODEL COMPARISON")
print("==========================================")

print(
    results_df.to_string(
        index=False
    )
)


# ==========================================
# 18. FIND BEST MODEL
# ==========================================

best_index = results_df["F1 Score"].idxmax()

best_model_name = results_df.loc[
    best_index,
    "Model"
]

best_f1_score = results_df.loc[
    best_index,
    "F1 Score"
]

best_model = trained_models[
    best_model_name
]


print("\n==========================================")
print("BEST MODEL")
print("==========================================")

print("Best Model:", best_model_name)

print(
    "Best F1 Score:",
    round(best_f1_score, 4)
)


# ==========================================
# 19. CREATE OUTPUT FOLDERS
# ==========================================

os.makedirs(
    "models",
    exist_ok=True
)

os.makedirs(
    "outputs",
    exist_ok=True
)


# ==========================================
# 20. SAVE MODEL COMPARISON
# ==========================================

results_df.to_csv(
    "outputs/model_comparison.csv",
    index=False
)


# ==========================================
# 21. SAVE BEST MODEL
# ==========================================

joblib.dump(
    best_model,
    "models/best_churn_model.pkl"
)


# ==========================================
# 22. FINAL OUTPUT
# ==========================================

print("\n==========================================")
print("FILES SAVED SUCCESSFULLY")
print("==========================================")

print(
    "\nModel comparison saved at:"
)

print(
    "outputs/model_comparison.csv"
)

print(
    "\nBest trained model saved at:"
)

print(
    "models/best_churn_model.pkl"
)


print("\n==========================================")
print("TELECOM CUSTOMER CHURN MODEL COMPLETED!")
print("==========================================")