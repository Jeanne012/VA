import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("ESG Sustainability Assessment for Non-Life Insurance Products")
st.write("Answer the questions below to assess the ESG sustainability of your insurance product.")

# Define ESG questionnaire with subcategories
questions = {
    "Underwriting & Product Design": {
        "Environmental": [
            "Does the policy exclude fossil-fuel-intensive assets?",
            "Does the policy incentivize low-carbon infrastructure (e.g., green buildings, EVs)?",
            "Does the policy integrate climate adaptation measures?"
        ],
        "Social": [
            "Does the policy ensure fair pricing for vulnerable populations?",
            "Are there non-discriminatory criteria in underwriting?",
            "Does the product promote financial inclusion?"
        ],
        "Governance": [
            "Are sustainability risks considered in underwriting decisions?",
            "Does the policy include transparency in ESG claims?",
            "Is there independent verification of ESG factors in product design?"
        ]
    },
    "Claims Management": {
        "Environmental": [
            "Does the claims process encourage repair over replacement?",
            "Are recycled or sustainable materials prioritized in claims?",
            "Is energy efficiency considered in damage compensation?"
        ],
        "Social": [
            "Is there a structured appeal process for denied claims?",
            "Are claims settled fairly and without bias?",
            "Are there support services for customers affected by extreme weather events?"
        ],
        "Governance": [
            "Are anti-fraud measures in place to ensure fair claims processing?",
            "Is there third-party oversight of claims handling?",
            "Does the company provide transparency in claims resolutions?"
        ]
    },
    "Asset & Premium Management": {
        "Environmental": [
            "Does the company divest from high-carbon investments?",
            "Are ESG principles integrated into investment decisions?",
            "Are investments aligned with climate transition goals?"
        ],
        "Social": [
            "Does the company invest in social impact initiatives?",
            "Are community-oriented investments prioritized?",
            "Does the investment strategy align with DEI principles?"
        ],
        "Governance": [
            "Does the company publicly disclose ESG performance?",
            "Are ESG-linked executive incentives in place?",
            "Is the ESG investment strategy reviewed by an independent body?"
        ]
    }
}

# Store responses
responses = {}
st.subheader("Answer the following Yes/No questions:")
for category, subcategories in questions.items():
    st.markdown(f"## {category}")  # Display category as a large header
    cols = st.columns(3)  # Create three columns for E, S, G
    i = 0
    for subcategory, qs in subcategories.items():
        with cols[i]:
            st.markdown(f"### {subcategory}")  # Display subcategory inside its own column
            for q in qs:
                responses[q] = st.radio(q, ("Yes", "No"), key=q)  # Add unique key to prevent errors
        i += 1

# Compute ESG score
score = sum(1 for response in responses.values() if response == "Yes")
total_questions = len(responses)
percentage = (score / total_questions) * 100

# Assign sustainability rating
if percentage >= 80:
    rating = "Green - Highly Sustainable"
elif percentage >= 50:
    rating = "Silver - Moderately Sustainable"
else:
    rating = "Bronze - Needs Improvement"

# Display results
st.subheader("Sustainability Score")
st.write(f"Your product scored: {score} out of {total_questions} ({percentage:.2f}%)")
st.success(f"Sustainability Rating: {rating}")

# Visualization
st.subheader("Score Visualization")
fig, ax = plt.subplots()
ax.barh(["Sustainability Score"], [percentage], color="green")
ax.set_xlim(0, 100)
ax.set_xlabel("Percentage")
ax.set_title("Sustainability Score")
st.pyplot(fig)

# Instructions for running the app
st.write("To run this app from GitHub:")
st.code("""
1. Install Streamlit: `pip install streamlit`
2. Run the app: `streamlit run esg_framework.py`
""", language="bash")
