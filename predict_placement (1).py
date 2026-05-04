# ### Comprehensive Project Explanation
# 
# This project details an end-to-end Machine Learning workflow focused on predicting student placement status. Below is a detailed breakdown of each stage:
# 
# ```
# # 1. Data Ingestion and Initial Exploration
# #    - Objective: Understand the raw data's structure and characteristics.
# #    - Source: Data is loaded from 'placementdata.csv'.
# #    - Initial Checks:
# #        - `df.head()`, `df.tail()`: Preview the first and last few rows.
# #        - `df.info()`: Get a summary of the DataFrame, including data types and non-null values.
# #        - `df.describe()`: Obtain descriptive statistics for numerical columns (count, mean, std, min, max, quartiles).
# #        - The initial inspection confirms a dataset with various student attributes and a 'PlacementStatus' target.
# 
# # 2. Data Preprocessing and Cleaning
# #    - Objective: Prepare the raw data for machine learning models.
# #    - Label Encoding:
# #        - Categorical features like 'ExtracurricularActivities', 'PlacementTraining', and 'PlacementStatus' are converted into numerical format (0 and 1).
# #        - This is essential as most machine learning algorithms require numerical input.
# #        - Tool Used: `sklearn.preprocessing.LabelEncoder`.
# #    - Missing Value Handling:
# #        - A check (`df.isnull().sum()`) is performed to identify and quantify any missing data.
# #        - In this dataset, no missing values were found, simplifying this stage.
# #    - Feature Identification:
# #        - Columns are explicitly classified as numerical or categorical.
# #        - `StudentID` is identified but excluded from features, and `PlacementStatus` is set as the target variable.
# #    - Skewness Analysis:
# #        - Skewness for numerical features is calculated and examined.
# #        - While 'PlacementTraining' showed high negative skewness, it's a binary encoded feature, so no transformation was deemed necessary.
# #        - This step helps in understanding data distribution and potential need for transformations.
# #    - Scaling:
# #        - Numerical features are scaled to a common range (0-1) using `MinMaxScaler`.
# #        - Prior scaling was done with `StandardScaler` (Z-score normalization), but was later replaced by `MinMaxScaler` as requested.
# #        - Scaling prevents features with larger numerical ranges from unduly influencing model training.
# 
# # 3. Data Visualization
# #    - Objective: Visually explore data distributions, relationships, and patterns.
# #    - Plots Generated:
# #        - **Distribution of Placement Status**: A count plot shows the balance (or imbalance) between placed and not-placed students.
# #        - **Correlation Heatmap**: Visualizes the correlation matrix of all numerical features, identifying highly correlated variables.
# #        - **Distribution of CGPA**: A histogram with KDE shows the distribution shape of CGPA.
# #        - **Box Plots (Placement Status vs. Features)**: These plots compare the distribution of key features (CGPA, AptitudeTestScore, Internships, Projects, Workshops/Certifications, SoftSkillsRating, SSC_Marks, HSC_Marks) across the 'Placed' and 'Not Placed' categories. This highlights features that differentiate between the two groups.
# #    - Tools Used: `matplotlib.pyplot` and `seaborn`.
# 
# # 4. Feature Engineering
# #    - Objective: Create new, more informative features from existing ones to potentially improve model performance.
# #    - New Features Created:
# #        - `AcademicPerformanceIndex`: An average of `CGPA`, `HSC_Marks`, and `SSC_Marks`. This consolidates academic achievements into a single metric.
# #        - `OverallSkillScore`: An average of `AptitudeTestScore` and `SoftSkillsRating`. This combines general aptitude and personal skills.
# #    - Scaling of New Features: These engineered features are also scaled using `MinMaxScaler` to ensure consistency with other features.
# 
# # 5. Feature Selection and Dimensionality Reduction
# #    - Objective: Reduce noise, combat the curse of dimensionality, and speed up training while retaining important information.
# #    - Feature Importance:
# #        - A `RandomForestClassifier` is trained to determine the importance of each feature in predicting placement status.
# #        - Key predictors identified: `HSC_Marks`, `AptitudeTestScore`, `SSC_Marks`, and `CGPA`.
# #    - Irrelevant Feature Removal:
# #        - Based on low importance scores, 'PlacementTraining' and 'Internships' are removed from the feature set.
# #    - Principal Component Analysis (PCA):
# #        - PCA is applied to transform the remaining features into a smaller set of uncorrelated components.
# #        - The number of components (e.g., 8) is chosen by analyzing the cumulative explained variance ratio, aiming to capture most of the dataset's variance with fewer features.
# #        - This helps in mitigating multicollinearity and reducing computational complexity.
# 
# # 6. Data Splitting
# #    - Objective: Divide the dataset into subsets for training and evaluating models.
# #    - Split Ratio: The dataset is split into 80% for training and 20% for testing.
# #    - Reproducibility: A `random_state` is used in `train_test_split` to ensure consistent splits across runs.
# #    - Purpose: Training on one set and evaluating on another provides an unbiased estimate of model performance on unseen data.
# 
# # 7. Model Training and Evaluation
# #    - Objective: Train various classification models and assess their performance.
# #    - Models Explored:
# #        - RandomForestClassifier
# #        - Logistic Regression (initial and optimized)
# #        - Decision Tree Classifier
# #        - XGBoost Classifier
# #        - Voting Classifier (an ensemble method combining multiple models)
# #        - AdaBoost Classifier
# #        - Gradient Boosting Classifier
# #    - Hyperparameter Tuning:
# #        - `GridSearchCV` is employed for `Logistic Regression` to find the optimal hyperparameters (e.g., `C=0.1`, `penalty='l1'`, `solver='liblinear'`) using cross-validation. This improves model generalization.
# #    - Evaluation Metrics:
# #        - **Confusion Matrices**: Visual representations showing True Positives, True Negatives, False Positives, and False Negatives.
# #        - **Classification Reports**: Detailed metrics including precision, recall, F1-score, and support for both 'Placed' (1) and 'Not Placed' (0) classes, along with overall accuracy.
# #        - These metrics provide a comprehensive understanding of each model's strengths and weaknesses.
# 
# # 8. Model Comparison and Selection
# #    - Objective: Identify the best-performing model based on evaluation metrics.
# #    - Comparison Table: A consolidated DataFrame of classification report metrics is generated, allowing for a direct comparison of all models.
# #    - Best Model: The `Optimized Logistic Regression`, `AdaBoost`, `Gradient Boosting`, and `Voting Classifier` models all achieved an accuracy of ~79% on the test set, indicating similar strong performance for this dataset.
# 
# # 9. Model Persistence and Deployment Readiness
# #    - Objective: Save the trained models for future use and prepare for deployment.
# #    - Individual Model Saving:
# #        - The best-performing `Optimized Logistic Regression` model is saved as `best_logistic_regression_model.joblib`.
# #    - Full ML Pipeline Creation and Saving:
# #        - A `scikit-learn` `Pipeline` is constructed to encapsulate the entire preprocessing workflow (feature removal, scaling, PCA) along with the final optimized `Logistic Regression` model.
# #        - This `full_pipeline` is saved as `full_ml_pipeline_model.joblib`. This is crucial for ensuring that new, raw data undergoes the exact same transformations as the training data before prediction, preventing data leakage and inconsistencies.
# #    - Pipeline Verification:
# #        - The saved `full_ml_pipeline_model.joblib` is loaded and its performance is verified on the test set to confirm successful persistence and functionality.
# #    - Deployment Script (`predict_placement.py`):
# #        - A Python script (`predict_placement.py`) is generated. This script demonstrates how to load the saved `full_ml_pipeline_model.joblib`, prepare new raw data (including label encoding and feature engineering as done during training), and use the pipeline to make predictions.
# #        - This script is designed for seamless integration into production environments, such as a Visual Studio application, making the ML solution portable and deployable.
# 
# # Conclusion:
# # This project demonstrates a robust, reproducible, and deployable machine learning solution for predicting student placement status, covering all essential stages from data understanding to model deployment.
# ```

import joblib
import pandas as pd
import numpy as np

# --- Mappings for Label Encoding (derived from original data) ---
# 'No': 0, 'Yes': 1 for both
EXTRACURRICULAR_MAPPING = {'No': 0, 'Yes': 1}
PLACEMENT_TRAINING_MAPPING = {'No': 0, 'Yes': 1}

# --- Expected feature order for the pipeline after preprocessing ---
# This list includes the original features that are not dropped, plus the engineered features.
EXPECTED_FEATURES = [
    'CGPA', 'Projects', 'Workshops/Certifications', 'AptitudeTestScore',
    'SoftSkillsRating', 'ExtracurricularActivities_encoded', 'SSC_Marks', 'HSC_Marks',
    'AcademicPerformanceIndex', 'OverallSkillScore'
]

def load_model(model_path):
    """Loads the saved machine learning pipeline model."""
    try:
        model = joblib.load(model_path)
        print(f"Model loaded successfully from '{model_path}'")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def prepare_new_data(raw_data: dict) -> pd.DataFrame:
    """Applies necessary preprocessing steps (label encoding, feature engineering) to raw input data.
    The raw_data dictionary should contain the original feature names before encoding/engineering.
    """
    # Convert raw_data to DataFrame
    df = pd.DataFrame([raw_data])

    # Apply Label Encoding using predefined mappings
    df['ExtracurricularActivities'] = df['ExtracurricularActivities'].map(EXTRACURRICULAR_MAPPING)
    df['PlacementTraining'] = df['PlacementTraining'].map(PLACEMENT_TRAINING_MAPPING)

    # Feature Engineering (as done in the notebook)
    df['AcademicPerformanceIndex'] = (df['CGPA'] + df['HSC_Marks'] + df['SSC_Marks']) / 3
    df['OverallSkillScore'] = (df['AptitudeTestScore'] + df['SoftSkillsRating']) / 2

    # Handle potential missing StudentID column if it's not provided in raw_data
    if 'StudentID' in df.columns:
        df = df.drop(columns=['StudentID'])

    # The pipeline was trained on features after dropping 'Internships' and 'PlacementTraining'
    # The ColumnTransformer in the pipeline handles the 'drop_least_important' step
    # So, we pass the features that were present in X *before* the pipeline's ColumnTransformer.
    # The ColumnTransformer itself will handle dropping the specified columns from its input.

    # Rename encoded categorical columns to match the names expected by the ColumnTransformer's numerical_features list.
    # Note: The ColumnTransformer was defined to scale `numerical_features` which included
    # 'ExtracurricularActivities' and 'PlacementTraining' after they were label encoded.
    # To align with how the ColumnTransformer was set up, we should ensure these are treated as numerical
    # and that the 'drop_least_important' step correctly removes 'PlacementTraining' and 'Internships'.
    # The numerical_features list in the notebook did NOT include 'Internships' and 'PlacementTraining'
    # after the initial removal, so let's re-verify the input to the preprocessor. No, the numerical_features
    # list *did* include them originally, and the `drop_least_important` handled removal.

    # Let's verify the columns of X_train *after* label encoding and feature engineering,
    # but *before* the full_pipeline's internal ColumnTransformer.
    # X_train had ['CGPA', 'Internships', 'Projects', 'Workshops/Certifications', 'AptitudeTestScore',
    # 'SoftSkillsRating', 'ExtracurricularActivities', 'PlacementTraining', 'SSC_Marks', 'HSC_Marks',
    # 'AcademicPerformanceIndex', 'OverallSkillScore']

    # Ensure column order and types match training data
    # For this script, we'll keep the column names as they were in X before the pipeline's ColumnTransformer
    # and let the pipeline itself handle the dropping of 'PlacementTraining' and 'Internships'.
    # This is critical for the `preprocessor` step in the pipeline.
    final_columns = [
        'CGPA', 'Internships', 'Projects', 'Workshops/Certifications', 'AptitudeTestScore',
        'SoftSkillsRating', 'ExtracurricularActivities', 'PlacementTraining', 'SSC_Marks', 'HSC_Marks',
        'AcademicPerformanceIndex', 'OverallSkillScore'
    ]

    # Select and reorder columns
    try:
        processed_df = df[final_columns]
    except KeyError as e:
        print(f"Missing expected feature in input data: {e}")
        return None

    return processed_df

def main():
    model_path = 'full_ml_pipeline_model.joblib'
    pipeline = load_model(model_path)

    if pipeline is None:
        return

    # Example new, raw student data (before any encoding or feature engineering)
    # This dictionary represents a single student's profile as it would appear
    # in the original 'placementdata.csv' file, but without 'StudentID' or 'PlacementStatus'.
    # All categorical features should be strings ('Yes', 'No') as they were originally.
    new_student_raw_data = {
        'CGPA': 7.8, # Raw CGPA, not scaled
        'Internships': 1, # Raw count
        'Projects': 2, # Raw count
        'Workshops/Certifications': 1, # Raw count
        'AptitudeTestScore': 75, # Raw score
        'SoftSkillsRating': 4.1, # Raw rating
        'ExtracurricularActivities': 'Yes', # Raw string: 'Yes' or 'No'
        'PlacementTraining': 'No', # Raw string: 'Yes' or 'No'
        'SSC_Marks': 70, # Raw score
        'HSC_Marks': 80 # Raw score
    }

    print("\nRaw input data for prediction:")
    print(new_student_raw_data)

    # Prepare the new data using the defined function
    prepared_data = prepare_new_data(new_student_raw_data)

    if prepared_data is None:
        print("Failed to prepare data. Cannot make prediction.")
        return

    print("\nPrepared data (after encoding and feature engineering, before pipeline's internal scaling/PCA):")
    print(prepared_data)

    # Make prediction
    prediction = pipeline.predict(prepared_data)
    prediction_proba = pipeline.predict_proba(prepared_data)

    print(f"\nPredicted Placement Status: {prediction[0]} (0: Not Placed, 1: Placed)")
    print(f"Prediction Probabilities: {prediction_proba[0]} (Probability for 0, Probability for 1)")

if __name__ == '__main__':
    main()
