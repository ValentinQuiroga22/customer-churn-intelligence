import pandas as pd
import streamlit as st

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Customer Churn Intelligence", page_icon="📊", layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("data/processed/customer_risk_scoring_business.csv")

# ==========================================
# CHURN DRIVER FUNCTION
# ==========================================


def explain_customer(customer):

    reasons = []

    if customer["Contract"] == "Month-to-month":
        reasons.append("Month-to-month contract")

    if customer["InternetService"] == "Fiber optic":
        reasons.append("Fiber optic internet service")

    if customer["OnlineSecurity"] == "No":
        reasons.append("No online security service")

    if customer["PaymentMethod"] == "Electronic check":
        reasons.append("Electronic check payment method")

    if customer["tenure"] < 12:
        reasons.append("Short customer tenure")

    return reasons


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Customer Selection")

customer_id = st.sidebar.selectbox("Select Customer", df["customerID"])

# ==========================================
# SELECT CUSTOMER
# ==========================================

customer = df[df["customerID"] == customer_id].iloc[0]

drivers = explain_customer(customer)

# ==========================================
# TITLE
# ==========================================

st.title("📊 Customer Churn Intelligence")

st.caption("Machine Learning + SHAP + Gemini")

st.divider()

# ==========================================
# CUSTOMER OVERVIEW
# ==========================================

st.subheader("Customer Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Customer ID", value=customer["customerID"])

with col2:
    st.metric(label="Risk Score", value=f"{customer['RiskScore']:.1%}")

with col3:
    st.metric(label="Risk Level", value=customer["RiskLevel"])

# ==========================================
# RISK BAR
# ==========================================

st.subheader("Risk Probability")

st.progress(float(customer["RiskScore"]))

# ==========================================
# MAIN DRIVERS
# ==========================================

st.subheader("Main Churn Drivers")

if len(drivers) > 0:
    for driver in drivers:
        st.info(driver)

else:
    st.success("No major churn drivers detected.")

# ==========================================
# CUSTOMER PROFILE
# ==========================================

st.subheader("Customer Profile")

profile = pd.DataFrame(
    {
        "Attribute": [
            "Contract",
            "Internet Service",
            "Payment Method",
            "Tenure",
            "Monthly Charges",
            "Online Security",
            "Tech Support",
        ],
        "Value": [
            customer["Contract"],
            customer["InternetService"],
            customer["PaymentMethod"],
            customer["tenure"],
            customer["MonthlyCharges"],
            customer["OnlineSecurity"],
            customer["TechSupport"],
        ],
    }
)

st.dataframe(profile, use_container_width=True, hide_index=True)

# ==========================================
# RAW DATA (OPTIONAL)
# ==========================================

with st.expander("View Full Customer Data"):
    st.dataframe(customer.to_frame(), use_container_width=True)
