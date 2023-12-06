import streamlit as st
import pandas as pd

def calculate_earnings(monthly_budget, pricing, impressions_per_100_dollars, conversion_rate, churn_rate, months=36):
    # Initialize list to store data for each month
    data = []

    total_customers = 0
    cumulative_revenue = 0
    cumulative_users = 0

    for month in range(1, months + 1):
        # Estimating ad reach based on budget
        ad_reach = int((monthly_budget / 100) * impressions_per_100_dollars)  # Convert to integer to remove decimals

        # Calculate monthly new customers based on ad reach and conversion rate
        monthly_new_customers = int(ad_reach * conversion_rate)  # Rounding down to nearest integer

        # Customers who churn
        churned_customers = int(total_customers * churn_rate)  # Rounding down to nearest integer

        # Update total customers
        total_customers = total_customers + monthly_new_customers - churned_customers
        total_customers = max(total_customers, 0)  # Ensure total customers don't go negative

        # Update cumulative users
        cumulative_users += monthly_new_customers

        # Monthly revenue
        monthly_revenue = int(total_customers * (pricing / 12))  # Monthly revenue based on annual pricing

        # Update cumulative revenue
        cumulative_revenue += monthly_revenue

        # Append to list
        data.append({
            'Month': month,
            'Ad Reach': ad_reach,
            'New Customers': monthly_new_customers,
            'Total Customers': total_customers,
            'Monthly Revenue (USD)': f'${monthly_revenue:7d}',  # Right align and remove decimals
            'Cumulative Revenue (USD)': f'${cumulative_revenue:10d}',  # Right align and remove decimals
            'Cumulative Users': cumulative_users
        })

    # Create DataFrame from the list
    df = pd.DataFrame(data)

    return df

# Streamlit UI
st.title("SaaS Earnings and Growth Forecast")

# User Inputs
pricing = st.sidebar.number_input("Annual Pricing (USD)", min_value=1, value=9)
monthly_budget = st.sidebar.number_input("Monthly Marketing Budget (USD)", min_value=0, value=100)  # Default set to $100
impressions_per_100_dollars = st.sidebar.number_input("Impressions per $100", value=6711)  # Default value based on CPM
conversion_rate = st.sidebar.number_input("Conversion Rate (as decimal)", min_value=0.0, max_value=1.0, value=0.03)  # Example default
churn_rate = st.sidebar.number_input("Churn Rate (as decimal)", min_value=0.0, max_value=1.0, value=0.02)  # Example default
months_to_forecast = st.sidebar.slider("Forecast Duration (Months)", 1, 36, 36)

if st.sidebar.button("Calculate Forecast"):
    forecast_df = calculate_earnings(monthly_budget, pricing, impressions_per_100_dollars, conversion_rate, churn_rate, months=months_to_forecast)
    st.write("Forecast for the next", months_to_forecast, "months:")
    st.table(forecast_df)

st.sidebar.markdown("### Assumptions and Inputs")
st.sidebar.markdown(f"- Pricing: ${pricing} per year")
st.sidebar.markdown(f"- Monthly Marketing Budget: ${monthly_budget}")
st.sidebar.markdown(f"- Impressions per $100: {impressions_per_100_dollars}")
st.sidebar.markdown(f"- Average Conversion Rate: {conversion_rate * 100}%")
st.sidebar.markdown(f"- Average Churn Rate: {churn_rate * 100}%")
