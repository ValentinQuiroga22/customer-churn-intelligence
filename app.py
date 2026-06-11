import pandas as pd
import streamlit as st

from src.report_utils import recommend_actions, build_llm_prompt

from src.llm_report_generator import generate_llm_report

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
# BUSINESS ACTIONS
# ==========================================


def recommend_business_actions(drivers):

    actions = []

    if "Short customer tenure" in drivers:
        actions.append("Launch onboarding retention campaign")

    if "Fiber optic internet service" in drivers:
        actions.append("Review customer satisfaction with Fiber Optic service")

    if "Electronic check payment method" in drivers:
        actions.append("Promote automatic payment methods")

    if "Month-to-month contract" in drivers:
        actions.append("Offer discount for annual contracts")

    return actions


# ==========================================
# BUILD STREAMLIT PROMPT
# ==========================================


def build_streamlit_prompt(customer_id, risk_score, drivers, actions):

    drivers_text = "\n".join([f"- {driver}" for driver in drivers])

    actions_text = "\n".join([f"- {action}" for action in actions])

    prompt = f"""
You are a Customer Retention Analyst.

Use ONLY the information provided.

Do not invent customer history.
Do not invent customer behavior.

Customer ID: {customer_id}

Risk Score: {risk_score:.1%}

Main Churn Drivers:

{drivers_text}

Recommended Actions:

{actions_text}

Create a concise business report.

Format:

Executive Summary

Risk Assessment

Recommended Actions

Maximum length: 150 words.
"""

    return prompt


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Customer Selection")

# Risk filter

risk_filter = st.sidebar.selectbox("Risk Level", ["All", "High", "Medium", "Low"])

if risk_filter == "All":
    filtered_df = df.copy()

else:
    filtered_df = df[df["RiskLevel"] == risk_filter]

# Customer search

search_customer = st.sidebar.text_input("Search Customer ID")

if search_customer:
    filtered_df = filtered_df[
        filtered_df["customerID"].str.contains(search_customer, case=False, na=False)
    ]

# Empty result protection

if filtered_df.empty:
    st.warning("No customers found.")

    st.stop()

# Customer selector

customer_id = st.sidebar.selectbox("Select Customer", filtered_df["customerID"])

# ==========================================
# SELECT CUSTOMER
# ==========================================

customer = filtered_df[filtered_df["customerID"] == customer_id].iloc[0]

drivers = explain_customer(customer)

# ==========================================
# TITLE
# ==========================================

st.title("📊 Customer Churn Intelligence")

st.caption("Machine Learning + SHAP + Gemini")

st.divider()

# ==========================================
# PORTFOLIO DASHBOARD
# ==========================================

total_customers = len(df)

high_risk = len(df[df["RiskLevel"] == "High"])

medium_risk = len(df[df["RiskLevel"] == "Medium"])

low_risk = len(df[df["RiskLevel"] == "Low"])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", total_customers)

with col2:
    st.metric("High Risk", high_risk)

with col3:
    st.metric("Medium Risk", medium_risk)

with col4:
    st.metric("Low Risk", low_risk)

st.divider()

# ==========================================
# TOP HIGH RISK CUSTOMERS
# ==========================================

st.subheader("Top 10 High Risk Customers")

top_risk = df.sort_values("RiskScore", ascending=False)[
    ["customerID", "RiskScore", "RiskLevel"]
].head(10)

top_risk["RiskScore"] = (top_risk["RiskScore"] * 100).round(1)

st.dataframe(top_risk, use_container_width=True, hide_index=True)

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
# AI REPORT
# ==========================================

st.subheader("AI Executive Report")

if st.button("Generate AI Report"):
    actions = recommend_business_actions(drivers)

    prompt = build_streamlit_prompt(
        customer_id=customer["customerID"],
        risk_score=customer["RiskScore"],
        drivers=drivers,
        actions=actions,
    )

    with st.spinner("Generating report..."):
        report = generate_llm_report(prompt)

        st.success("AI Report Generated")

    st.markdown(report)

    st.download_button(
        label="📄 Download Report",
        data=report,
        file_name=f"customer{customer['customerID']}_churn_report.txt",
        mime="text/plain",
    )


# ==========================================
# RAW DATA
# ==========================================

with st.expander("View Full Customer Data"):
    st.dataframe(customer.to_frame(), use_container_width=True)
