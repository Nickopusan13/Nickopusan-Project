# Penguin Species Classification
This project [`Penguin.ipynb`](Penguin.ipynb) uses a dataset of penguin measurements to predict species (Adelie, Gentoo, Chinstrap) with a Random Forest Classifier.

## Dataset
- Source: `penguins.csv`
- Features: Bill length, bill depth, flipper length, body mass, sex
- Target: Species (encoded: 0=Adelie, 1=Chinstrap, 2=Gentoo)

## Workflow
1. **Data Cleaning**: Handled missing values (mean for numeric, mode for categorical).
2. **Preprocessing**: Encoded categorical variables, scaled features, and oversampled the training set.
3. **Visualization**: Bar plots of mean measurements per species.
4. **Model**: Trained a Random Forest Classifier (100 trees).
5. **Evaluation**: Achieved 100% test accuracy and 98.9% cross-validation score.
6. **Insights**: Bill length and flipper length were the most important features.

## Key Skills
- Data cleaning and preprocessing
- Visualization with Seaborn/Matplotlib
- Supervised learning with Scikit-learn
- Handling class imbalance with oversampling

## Results
- Test Accuracy: 100%
- Mean CV Score: 98.9%
- Top Features: Bill length (35.23%), Flipper length (27.18%)
