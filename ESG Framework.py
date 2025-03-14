import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    
    # Create three expandable boxes for E, S, G
    for subcategory, qs in subcategories.items():
        with st.expander(subcategory):
            for q in qs:
                responses[q] = st.radio(q, ("Yes", "No"), key=q, index=None)  # Add unique key to prevent errors

# Compute ESG score per category
category_scores = {category: {"Environmental": 0, "Social": 0, "Governance": 0} for category in questions}
for category, subcategories in questions.items():
    for subcategory, qs in subcategories.items():
        category_scores[category][subcategory] = sum(1 for q in qs if responses[q] == "Yes")

# Compute overall ESG score
total_yes = sum(sum(sub.values()) for sub in category_scores.values())
total_questions = sum(len(sub[subcat]) for sub in questions.values() for subcat in sub)
percentage = (total_yes / total_questions) * 100 if total_questions > 0 else 0  # Avoid division by zero

# Assign sustainability rating
if percentage >= 80:
    rating = "Green - Highly Sustainable"
elif percentage >= 50:
    rating = "Silver - Moderately Sustainable"
else:
    rating = "Bronze - Needs Improvement"

# Display results in an expandable box
st.markdown("## Sustainability Score")
with st.expander("See Results"):
    st.write(f"Your product scored: {total_yes} out of {total_questions} ({percentage:.2f}%)")
    st.success(f"Sustainability Rating: {rating}")

    # Stacked bar chart visualization
    st.subheader("Score Distribution by Category")
    categories = list(category_scores.keys())
    environmental_scores = [category_scores[cat]["Environmental"] for cat in categories]
    social_scores = [category_scores[cat]["Social"] for cat in categories]
    governance_scores = [category_scores[cat]["Governance"] for cat in categories]

    fig, ax = plt.subplots()
    bar_width = 0.5
    bottom = np.zeros(len(categories))
    ax.bar(categories, environmental_scores, bar_width, label='Environmental', color='#2E7D32', bottom=bottom)
    bottom += environmental_scores
    ax.bar(categories, social_scores, bar_width, label='Social', color='#66BB6A', bottom=bottom)
    bottom += social_scores
    ax.bar(categories, governance_scores, bar_width, label='Governance', color='#A5D6A7', bottom=bottom)

    ax.set_ylabel("Percentage of Yes Responses")
    ax.set_title("Stacked Bar Chart of ESG Scores")
    ax.legend(["Environmental", "Social", "Governance"], loc='upper right', fontsize=10, frameon=False)
    ax.tick_params(axis='x', labelsize=8)  # Reduce label size
    st.pyplot(fig)

