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
            "Does the policy promote the decarbonization of the product portfolio (e.g., excluding fossil-fuel-intensive assets)?",
            "Does the policy provide coverage for resilient infrastructure and climate adaptation incentives?",
            "Does the policy promote sustainable resource use (e.g., repair-first approach, use of recycled materials)?"
        ],
        "Social": [
            "Does the policy ensure fair pricing models for low-income policyholders?",
            "Does the underwriting process ensure non-discriminatory and equitable access?",
            "Does the policy promote consumer protection through clear and transparent ethical terms?"
        ],
        "Governance": [
            "Are ESG risks integrated into underwriting decisions?",
            "Does the policy include independent verification of ESG factors?",
            "Does the policy prevent greenwashing by ensuring transparent sustainability claims?"
        ]
    },
    "Claims Management": {
        "Environmental": [
            "Does the claims process prioritize repair over replacement to reduce waste?",
            "Are recycled or sustainable materials encouraged in claims settlements?",
            "Are climate resilience measures integrated into claims management (e.g., rebuilding with green materials)?"
        ],
        "Social": [
            "Is there a structured appeal process for denied claims to ensure fairness?",
            "Are claims settled fairly and transparently, without bias?",
            "Does the claims process include support services for vulnerable customers (e.g., mental health post-incident support)?"
        ],
        "Governance": [
            "Are strong anti-fraud measures in place for claims processing?",
            "Is there third-party oversight ensuring fair and ethical claims handling?",
            "Does the company disclose its claims sustainability impact?"
        ]
    },
    "Asset & Premium Management": {
        "Environmental": [
            "Does the company divest from high-carbon investments and align with climate transition goals?",
            "Are ESG principles integrated into investment screening and decision-making?",
            "Does the company invest in biodiversity-friendly projects (e.g., reforestation, conservation)?"
        ],
        "Social": [
            "Does the company prioritize social impact investing in underprivileged communities?",
            "Are community-oriented investments aligned with stakeholder engagement initiatives?",
            "Does the investment strategy align with diversity, equity, and inclusion (DEI) principles?"
        ],
        "Governance": [
            "Does the company publicly disclose ESG performance and investment policies?",
            "Are ESG-linked executive incentives in place to ensure accountability?",
            "Is the ESG investment strategy reviewed by an independent sustainability body?"
        ]
    }
}

# Store responses
responses = {}
for category, subcategories in questions.items():
    st.markdown(f"### {category}")  # Display category as a large header
    
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

# Assign sustainability rating and corresponding color
if percentage >= 80:
    rating = "Green - Highly Sustainable"
    color = "green"
elif percentage >= 50:
    rating = "Silver - Moderately Sustainable"
    color = "silver"
else:
    rating = "Bronze - Needs Improvement"
    color = "#cd7f32"  # Bronze color

# Display results in an expandable box
st.markdown("### Sustainability Score")
with st.expander("See Results"):
    st.write(f"Your product scored: {total_yes} out of {total_questions} ({percentage:.2f}%)")
    st.markdown(f'<div style="background-color:{color};padding:10px;border-radius:5px;"><b>{rating}</b></div>', unsafe_allow_html=True)

    st.subheader("Score Distribution by Category")
    categories = list(category_scores.keys())
    max_possible_yes = max(sum(len(questions[cat][subcat]) for subcat in questions[cat]) for cat in categories)  # Maximum possible Yes per category

    environmental_scores = [category_scores[cat]["Environmental"] for cat in categories]
    social_scores = [category_scores[cat]["Social"] for cat in categories]
    governance_scores = [category_scores[cat]["Governance"] for cat in categories]

    fig, ax = plt.subplots()
    bar_width = 0.5
    bottom = np.zeros(len(categories))

    # Normalize values to fit within the maximum possible range
    ax.bar(categories, environmental_scores, bar_width, color='#2E7D32', bottom=bottom, label='Environmental')
    bottom += environmental_scores
    ax.bar(categories, social_scores, bar_width, color='#66BB6A', bottom=bottom, label='Social')
    bottom += social_scores
    ax.bar(categories, governance_scores, bar_width, color='#A5D6A7', bottom=bottom, label='Governance')

    ax.set_ylabel("Number of Yes Responses")
    ax.set_ylim(0, max_possible_yes)  # Ensuring y-axis max is per-category limit
    ax.set_title("Stacked Bar Chart of ESG Scores")
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.legend(["Environmental", "Social", "Governance"], loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10, frameon=True)

    st.pyplot(fig)

    
