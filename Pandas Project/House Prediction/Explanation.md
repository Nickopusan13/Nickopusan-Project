# House Price Prediction Using Machine Learning
### Introduction
This project [`House.ipynb`](House.ipynb) demonstrates a complete machine learning workflow for predicting house prices using the "House Test Data.csv" dataset. The objective is to develop and evaluate regression models that predict house prices based on features such as the number of bedrooms, bathrooms, square footage, and location. This README outlines the steps taken, the models used, and the skills demonstrated, making it a strong addition to my GitHub portfolio.

## Project Workflow
### 1. Data Loading and Initial Setup
Libraries Used: The project leverages `Python` libraries like `pandas` and `numpy` for data manipulation, `matplotlib` and `seaborn` for visualization, and `scikit-learn`, `xgboost`, and `lightgbm` for machine learning.
Dataset: The dataset includes features such as `price`, `bedrooms`, `bathrooms`, `sqft_living`, `street`, `city`, and `others`, loaded into a pandas DataFrame for analysis.
### 2. Data Preprocessing
Categorical Encoding: Categorical columns (date, street, city, statezip, country) are transformed into numerical values using LabelEncoder to prepare them for modeling.
Outlier Detection and Removal:
A boxplot visualizes the distribution of price to detect outliers.
Z-scores are computed, and rows with an absolute z-score ≥ 3 are dropped to remove extreme values.
Handling Missing Values:
Zero values are converted to NaN to identify missing data.
Columns with excessive missing values (yr_renovated, sqft_basement, view, waterfront) are removed.
Rows with remaining NaN values are dropped, and any leftover NaNs are filled with 0.
### 3. Feature Engineering
A new feature, price_per_sqft, is engineered by dividing price by sqft_living. This feature captures the price relative to living area, potentially enhancing the model’s predictive accuracy.
### 4. Data Preparation for Modeling
Feature and Target Split: The dataset is divided into features (x) and the target variable (y, which is price).
Scaling: Features are standardized using StandardScaler to ensure uniform scaling.
Train-Test Split: The data is split into training and testing sets (60-40 split) to evaluate model performance on unseen data.
### 5. Model Training and Evaluation
Several regression models are trained and assessed using Mean Absolute Error (MAE) and R² Score. The results are summarized below:

| Model                | MAE         | R²     |
|----------------------|-------------|--------|
| K-Nearest Neighbors  | 90,199.96   | 0.786  |
| Random Forest        | 8,726.10    | 0.994  |
| Gradient Boosting    | 15,177.74   | 0.995  |
| XGBoost              | 18,195.10   | 0.987  |
| LightGBM             | 18,042.33   | 0.990  |
| Linear Regression    | 59,973.30   | 0.878  |

### Key Insights:
Random Forest and Gradient Boosting excel with the lowest MAE and highest R² scores, indicating their ability to model complex relationships in the data.
Ensemble methods outperform simpler models like Linear Regression and KNN, making them ideal for this task.
## Why This Matters
This project highlights critical data science skills:

- Data Cleaning: Managing missing values and outliers to create a reliable dataset.
- Feature Engineering: Designing price_per_sqft to boost model performance.
- Modeling: Training and comparing multiple regression models to find the best fit.
- Evaluation: Using MAE and R² to measure model accuracy and goodness of fit.
- The strong performance of Random Forest and Gradient Boosting demonstrates the effectiveness of ensemble methods for house price prediction, showcasing practical machine learning expertise.

## Final Notes
The original dataset contained 4,600 rows and 18 columns, refined to 4,566 rows and 15 columns after preprocessing.
Future enhancements could include hyperparameter tuning or adding more features to further improve accuracy.
This project serves as a robust example of a structured, data-driven approach to regression problems, making it a valuable part of my portfolio.
