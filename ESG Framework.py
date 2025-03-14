import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("ESG Sustainability Assessment for Non-Life Insurance Products")
st.write("Answer the questions below to assess the ESG sustainability of your insurance product.")

# Define ESG questionnaire
questions = {
    "Underwriting & Product Design": [
        "Does the policy exclude fossil-fuel-intensive assets?",
        "Does the policy incentivize low-carbon infrastructure (e.g., green buildings, EVs)?",
        "Does the policy integrate climate adaptation measures?"
    ],
    "Claims Management": [
        "Does the claims process encourage repair over replacement?",
        "Are recycled or sustainable materials prioritized in claims?",
        "Is there a structured appeal process for denied claims?"
    ],
    "Asset & Premium Management": [
        "Does the company divest from high-carbon investments?",
        "Are ESG principles integrated into investment decisions?",
        "Does the company publicly disclose ESG performance?"
    ]
}

# Store responses
responses = {}
st.subheader("Answer the following Yes/No questions:")
for category, qs in questions.items():
    st.subheader(category)
    for q in qs:
        responses[q] = st.radio(q, ("Yes", "No"))

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
