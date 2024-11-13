import streamlit as st
import pandas as pd
from Merton import Merton

# Streamlit app
def main():
    st.title("Financial Metrics Calculator")
    st.write("""
    Input financial data to calculate key metrics:
    - Default Probability
    - Credit Spreads
    - Recovery Rate
    """)

    # Input form
    st.sidebar.header("Input Parameters")
    risk_free_rate = st.sidebar.number_input("Risk-Free Rate (%)", min_value=0.0, value=1.0, step=0.01) / 100
    time_to_default = st.sidebar.number_input("Time to Default (Years)", min_value=0.1, value=1.0, step=0.1)
    market_cap = st.sidebar.number_input("Market Cap ($ Million)", min_value=1.0, value=1000.0, step=10.0) * 1e6
    total_debt = st.sidebar.number_input("Total Debt ($ Million)", min_value=1.0, value=500.0, step=10.0) * 1e6
    company_volatility = st.sidebar.number_input("Company Volatility (%)", min_value=0.0, value=20.0, step=0.1) / 100

    if st.sidebar.button("Calculate Metrics"):
        # Run Merton Model
        merton_model = Merton(
            S=market_cap,
            V=market_cap + total_debt,
            D=total_debt,
            r=risk_free_rate,
            sigma_s=company_volatility,
            T=time_to_default
        )

        # Calculate Metrics
        default_proba = merton_model.default_proba()
        credit_spread = merton_model.credit_spread()
        recovery_rate = merton_model.recovery_rate()

        # Display Metrics
        st.subheader("Calculated Metrics")
        st.metric("Default Probability (%)", f"{default_proba:.2f}")
        st.metric("Credit Spread (bps)", f"{credit_spread * 10000:.2f}")
        st.metric("Recovery Rate (%)", f"{recovery_rate:.2f}")

if __name__ == "__main__":
    main()
