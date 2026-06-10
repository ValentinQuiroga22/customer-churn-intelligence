# ==========================================
# FEATURE MAPPING
# ==========================================

feature_mapping = {

    "tenure":
        "Short customer tenure",

    "InternetService_Fiber optic":
        "Fiber optic internet service",

    "PaymentMethod_Electronic check":
        "Electronic check payment method",

    "Contract_One year":
        "One-year contract",

    "Contract_Two year":
        "Two-year contract",

    "OnlineSecurity_No":
        "No online security service"
}

# ==========================================
# RECOMMEND ACTIONS
# ==========================================

def recommend_actions(
    positive_drivers
):

    actions = []

    features = positive_drivers["Feature"].tolist()

    if "tenure" in features:

        actions.append(
            "Launch onboarding retention campaign"
        )

    if "InternetService_Fiber optic" in features:

        actions.append(
            "Review customer satisfaction with Fiber Optic service"
        )

    if "PaymentMethod_Electronic check" in features:

        actions.append(
            "Promote automatic payment methods"
        )

    if (
        "Contract_One year" in features
        or
        "Contract_Two year" in features
    ):

        actions.append(
            "Offer discount for annual contracts"
        )

    return actions


# ==========================================
# CUSTOMER REPORT
# ==========================================

def generate_customer_report(
    customer_id,
    risk_score,
    positive_drivers
):

    report = f"""
CUSTOMER CHURN REPORT

Customer ID: {customer_id}

Risk Score: {risk_score:.1%}

Main Churn Drivers:
"""

    for feature in positive_drivers.head(5)["Feature"]:

        friendly_name = feature_mapping.get(
            feature,
            feature
        )

        report += f"\n- {friendly_name}"

    report += "\n\nRECOMMENDED ACTIONS:\n"

    actions = recommend_actions(
        positive_drivers
    )

    for action in actions:

        report += f"\n- {action}"

    return report


# ==========================================
# BUILD LLM PROMPT
# ==========================================

def build_llm_prompt(
    customer_id,
    risk_score,
    positive_drivers,
    actions
):

    drivers_text = "\n".join(

        [
            f"- {feature_mapping.get(feature, feature)}"
            for feature in positive_drivers.head(5)["Feature"]
        ]

    )

    actions_text = "\n".join(

        [
            f"- {action}"
            for action in actions
        ]

    )

    prompt = f"""
You are a Customer Retention Analyst.

Use ONLY the information provided below.

Do not invent customer history.
Do not invent customer behavior.
Do not invent reasons that are not listed.

Create a concise executive report.

Customer ID: {customer_id}

Risk Score: {risk_score:.1%}

Main Churn Drivers:

{drivers_text}

Recommended Actions:

{actions_text}

Output format:

Executive Summary

Risk Assessment

Recommended Actions

Maximum length: 150 words.
"""

    return prompt