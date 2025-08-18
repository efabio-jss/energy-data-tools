# Python Demo: Statistical Modelling + Anomaly Detection

This script is a **conceptual exercise** designed to showcase **data analyst / data science skills** in statistical modelling, machine learning, and anomaly detection.  
It builds an **end-to-end pipeline**: synthetic data → pre-processing → model → validation → anomaly detection → saved outputs.

---

## What the script does
1. **Generates synthetic data** for product pricing (with brand, age, condition, diameter, box/papers).
2. **Injects anomalies** (outlier prices and features) to simulate real-world messy data.
3. **Trains a Ridge regression model** on the *log-price* scale (hedonic model).
4. **Validates performance** with:
   - Holdout test set  
   - 5-fold cross-validation  
   - Bootstrap confidence intervals
5. **Detects anomalies** using:
   - Robust residual z-scores (based on MAD)  
   - IsolationForest (tree-based anomaly detector)
6. **Saves outputs** (`dataset.csv`, `anomalies_top20.csv`, residual plots, histograms, prediction plots).

---

## Key concepts explained

### Machine Learning
- **Definition**: Machine Learning (ML) is a subset of Artificial Intelligence where algorithms learn patterns from data to make predictions or decisions without being explicitly programmed with rules.  
- In this script: the Ridge regression model *learns* the relationship between product features (brand, age, etc.) and price.  
- ML differs from classic programming because the **rules are inferred from data**, not hard-coded.

### Hedonic Ridge Regression
- **Hedonic model**: A regression where price is explained by product characteristics.  
- **Ridge regression**: A linear regression with an *L2 penalty* on coefficients.  
  - Prevents overfitting and handles multicollinearity.  
  - Controlled by the hyperparameter `alpha`.  
  - Here we use **Ridge on log-price**:  
    \( \log(1 + price) = X\beta + \epsilon \).

### Log-transformation + Smearing (Duan)
- We train on \( \log(1+price) \) because prices are skewed.  
- When predicting, we re-transform back to price space using the **smearing estimator** (corrects bias from the log transform).

### Validation metrics
- **MAE (Mean Absolute Error)**: average absolute difference between predicted and true prices.  
  - Easy to interpret in units of the target.  
  - Lower = better.  
- **R² (Coefficient of determination)**: proportion of variance explained by the model.  
  - 1.0 = perfect fit, 0 = no better than mean.

### Bootstrap Confidence Intervals
- We resample the test set many times (with replacement).  
- Gives a **95% range** for metrics like MAE and R².  
- Shows *uncertainty* around model performance.

### Cross-validation (CV)
- Splits the dataset into folds.  
- Each fold is used once as test, the rest as train.  
- Reduces risk of overfitting to a single train/test split.

### Anomaly detection
- **Residuals**: difference between actual and predicted prices.  
- **Robust z-score**: like a z-score, but using the **median** and **MAD (Median Absolute Deviation)**, less sensitive to outliers.  
  - Large |z| ⇒ potential anomaly.  
- **IsolationForest**: ensemble method that isolates points by random splits.  
  - Outliers are easier to isolate (shorter paths in the trees).  
  - Outputs `-1` for anomaly, `1` for normal.

---

## Artifacts produced
- `dataset.csv` — synthetic dataset used.  
- `anomalies_top20.csv` — top anomalies detected.  
- `residuals_vs_pred.png` — residuals vs predicted values.  
- `residuals_rz_hist.png` — histogram of robust z-scores.  
- `true_vs_pred.png` — true vs predicted prices.

---

## Key points
- End-to-end workflow: **data → features → model → validation → anomalies → outputs**.  
- Why Ridge? Regularization makes the model more stable and realistic.  
- Why log-price? Prices are skewed; log stabilizes variance.  
- Why bootstrap + CV? Demonstrates awareness of **uncertainty** and **generalization**.  
- Why anomaly detection? Shows how to **identify suspicious records** (important in pricing, fraud, sensor data, etc.).  
- Clean code, reproducible pipeline, artifacts saved for inspection.

---

👉 This exercise demonstrates **practical applied skills** in:
- **Machine Learning** (modeling relationships in data)  
- **Statistical modeling** (hedonic regression, log-transform)  
- **Model evaluation** (MAE, R², bootstrap, CV)  
- **Anomaly detection** (residual analysis + IsolationForest)  
- **Reproducible data pipelines (Python + scikit-learn)**  
