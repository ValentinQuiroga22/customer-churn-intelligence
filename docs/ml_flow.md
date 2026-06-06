# Machine Learning Results & Business Insights

## Model Performance

A Logistic Regression model was trained to predict customer churn.

### Performance Metrics

| Metric | Value |
|----------|----------|
| Accuracy | 80.62% |
| Precision | 66% |
| Recall | 56% |
| F1 Score | 60% |

### Interpretation

At first glance, an accuracy of 80.6% appears strong. However, the dataset is imbalanced:

- 73.5% of customers did not churn
- 26.5% of customers churned

A naive model predicting every customer as "No Churn" would already achieve approximately 73.5% accuracy.

For this reason, additional metrics such as Precision, Recall, and F1 Score were evaluated.

---

## Classification Report

### Precision (66%)

When the model predicts that a customer will churn:

- 66% actually churn

This metric measures how reliable churn predictions are.

### Recall (56%)

Among all customers who actually churned:

- The model successfully identified 56%

This is particularly important because missed churn opportunities represent lost revenue.

### F1 Score (60%)

The F1 Score balances Precision and Recall and is useful when working with imbalanced datasets.

---

## Confusion Matrix

| Actual / Predicted | No Churn | Churn |
|--------------------|----------|--------|
| No Churn | 927 | 108 |
| Churn | 165 | 209 |

### Interpretation

#### True Negatives (927)

Customer stayed and the model correctly predicted retention.

#### True Positives (209)

Customer churned and the model correctly predicted churn.

#### False Positives (108)

The model predicted churn, but the customer stayed.

This represents unnecessary retention efforts.

#### False Negatives (165)

The customer churned but the model predicted retention.

These are missed intervention opportunities.

---

## Business Interpretation

The model correctly identified:

- 209 customers who eventually churned

out of:

- 374 total churned customers

This means the model detects approximately:

56% of customers at risk of leaving.

For a retention team, this provides a significant advantage over random targeting.

---

# Feature Importance Analysis

One advantage of Logistic Regression is interpretability.

Model coefficients allow us to understand which factors increase or decrease churn risk.

---

## Strongest Churn Drivers

| Feature | Coefficient |
|----------|------------:|
| InternetService_Fiber optic | 1.18 |
| TotalCharges | 0.53 |
| PaymentMethod_Electronic check | 0.39 |
| StreamingTV_Yes | 0.37 |
| PaperlessBilling_Yes | 0.37 |
| StreamingMovies_Yes | 0.37 |
| MultipleLines_Yes | 0.36 |

### Business Insight

Customers using Fiber Optic internet services and Electronic Check payment methods exhibit substantially higher churn risk.

These segments should be prioritized for retention analysis.

---

## Strongest Retention Drivers

| Feature | Coefficient |
|----------|------------:|
| Contract_Two year | -1.31 |
| tenure | -1.26 |
| Contract_One year | -0.68 |
| PhoneService_Yes | -0.52 |
| MonthlyCharges | -0.47 |
| OnlineSecurity_Yes | -0.35 |
| TechSupport_Yes | -0.30 |

### Business Insight

Long-term contracts and customer longevity are the strongest predictors of retention.

Customers with Online Security and Tech Support services are also significantly less likely to churn.

---

# Validation of Exploratory Analysis

The machine learning model validated the main findings discovered during EDA.

### Confirmed Findings

✓ Longer contracts reduce churn

✓ Customers with short tenure are more likely to leave

✓ Tech Support reduces churn

✓ Online Security reduces churn

✓ Electronic Check customers churn at higher rates

✓ Fiber Optic customers show elevated churn risk

This consistency increases confidence that these patterns are genuine business drivers rather than random correlations.

---

# Customer Risk Segmentation

Instead of generating only binary predictions, the model was used to estimate churn probability for each customer.

Customers were segmented into:

- Low Risk
- Medium Risk
- High Risk

based on predicted churn probability.

---

## Segment Distribution

| Risk Level | Customers |
|------------|-----------|
| Low Risk | 865 |
| Medium Risk | 335 |
| High Risk | 209 |

---

## Actual Churn Rate by Segment

| Risk Level | Stayed | Churned |
|------------|---------|----------|
| Low Risk | 89.5% | 10.5% |
| Medium Risk | 60.3% | 39.7% |
| High Risk | 28.2% | 71.8% |

---

## Business Value

The model successfully concentrates churn risk into the High Risk segment.

Customers classified as High Risk exhibit a churn rate of 71.8%, compared to only 10.5% in the Low Risk segment.

This allows retention teams to:

- Prioritize outreach efforts
- Reduce retention costs
- Improve campaign efficiency
- Allocate customer success resources more effectively

---

# Key Executive Takeaways

1. Contract duration is the strongest retention factor.

2. Customer tenure is one of the most important predictors of loyalty.

3. Fiber Optic customers show the highest churn propensity.

4. Electronic Check payment users represent a high-risk segment.

5. Online Security and Tech Support services improve retention.

6. The model identifies over half of all future churners before they leave.

7. High-risk customers churn nearly 7x more often than low-risk customers.

8. Churn prediction can be operationalized into customer risk scores for targeted retention campaigns.