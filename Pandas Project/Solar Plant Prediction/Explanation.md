# Solar Plant Failure Prediction Notebook
This repository contains a Jupyter Notebook ([`solar_plant.ipynb`](solar_plant.ipynb)) that demonstrates an end-to-end pipeline for detecting failure events in solar plants. The notebook covers data preparation, visualization, model training, evaluation, and finally, model persistence. Below is an overview of the main sections and processes:

## 1. Importing Libraries
The notebook begins by importing essential libraries, including:

- **Data Handling**: `pandas`, `numpy`

- **Visualization**: `matplotlib`, `seaborn`

- **Preprocessing & Model Selection**: Scikit-Learn modules such as `train_test_split`, `StandardScaler`, and `LabelEncoder`

- **Handling Imbalanced Data**: `RandomOverSampler` from `imblearn`

- **Machine Learning Model**: `XGBClassifier` from the XGBoost package

- **Model Persistence**: `joblib`

Additional utilities such as `warnings` (to ignore unnecessary warnings) are also configured.

## 2. Data Loading and Cleaning
- **Loading Data**: Data for multiple solar plants is loaded (e.g., from CSV files), and initial checks (like duplicate counts) are performed.

- **Filtering Failures**: The notebook filters the dataset to focus on potential failure events. For example, it selects rows where `AC_POWER` is zero during daytime (i.e., when the current hour is between the sunrise and sunset times).

## 3. Exploratory Data Analysis (EDA)
To understand the characteristics of failure events, the notebook creates histograms using Seaborn:

- **Humidity**: Distribution of humidity values during failures.

- **Radiation**: Distribution of radiation levels.

- **Temperature**: Distribution of temperature values.

- **Pressure**: Distribution of atmospheric pressure.

Each plot is labeled appropriately and combined into a 2x2 subplot layout, with a title summarizing that the graphs depict the "Distribution Failure."

## 4. Feature Engineering
- **Creating a Failure Flag**: A new binary column (`failure`) is created based on specific conditions:

  - `AC_POWER` equals 0.

  - `Humidity` is 80 or above.

  - `Radiation` is either below 200 or above 900.

  - The timestamp hour is between the sunrise and one hour before sunset.

- **Encoding Categorical Variables**: The `SOURCE_KEY` column is label encoded to transform any non-numeric identifiers into numerical values.

## 5. Data Splitting and Scaling
- **Splitting Data**: The dataset is split into training (60%), validation (20%), and test (20%) sets. The splits are stratified by the `failure` column to maintain the same class distribution across splits.

- **Scaling Features**: A helper function (`scale_dataset`) is defined to:

  - Drop irrelevant columns (e.g., `DATE_TIME`).

  - Scale features using `StandardScaler`.

  - Optionally apply oversampling (using `RandomOverSampler`) to the training set to handle any class imbalance.

## 6. Model Training
An XGBoost classifier (`XGBClassifier`) is set up with the following hyperparameters:

- **n_estimators**: 100

- **learning_rate**: 0.1

- **max_depth**: 3

- **random_state**: 42

The model is trained on the oversampled training data.

## 7. Model Evaluation
- **Test Set Predictions**: After training, the model makes predictions on the test set. A classification report is generated, which includes precision, recall, f1-score, and support for each class.

- **Cross-Validation**: 5-fold cross-validation is performed on the training data. For each fold, the score is printed along with the overall mean and standard deviation. This gives an idea of the model's robustness and stability across different data splits.

## 8. Model Persistence
Finally, the trained model is saved to a file (`SolarPlant.joblib`) using the `joblib` library. This allows for later reuse of the model without needing to retrain it.

## 9. How to Run
To run this notebook:

 1. Install the required libraries:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn xgboost joblib
```
 2. Open the notebook in Jupyter or any compatible IDE.
 3. Execute the cells in order to load the data, train the model, evaluate, and finally save the model.

## Conclusion
This notebook provides a comprehensive example of how to process and analyze solar plant data for failure detection. The workflow covers data preparation, exploratory analysis, feature engineering, model training, evaluation, and saving, which is useful for deploying predictive maintenance models in real-world scenarios.
