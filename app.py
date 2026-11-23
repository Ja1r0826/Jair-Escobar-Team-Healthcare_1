import streamlit as st
import pandas as pd
import numpy as np
import json
import math
from datetime import date
from dateutil.relativedelta import relativedelta

# --- 1. INITIALIZATION & BASELINE ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_date = date(2027, 1, 1)
    st.session_state.month_index = 1  # t=1 for seasonal math
    st.session_state.cash = 4000.00
    st.session_state.retained_earnings = -500.00  # Pre-opening expense
    st.session_state.last_result = None

    # Ledger to log all events and integer transactions
    st.session_state.ledger = [
        {"date": "2026-12-01", "description": "Owner Contribution", "category": "Financing", "amount": 6000.00},
        {"date": "2026-12-15", "description": "Equipment/Accessibility Assets", "category": "Capex", "amount": -1500.00},
        {"date": "2026-12-20", "description": "Pre-opening Setup Expense", "category": "Fixed Cost", "amount": -500.00}
    ]

# --- 2. SIDEBAR: BUSINESS METRICS ---
st.sidebar.title("Healthcare (NUR-2)")
st.sidebar.subheader(f"Current Date: {st.session_state.current_date.strftime('%B %Y')}")
st.sidebar.metric("Available Cash", f"${st.session_state.cash:,.2f}")
st.sidebar.metric("Retained Earnings", f"${st.session_state.retained_earnings:,.2f}")

# --- 3. MAIN DASHBOARD PANELS ---
tab1, tab2, tab3 = st.tabs(["Run Month", "Ledger & Finance", "Math Skills (Precalculus)"])

with tab1:
    st.header("Run Next Month's Operations")

    # Inputs
    price = st.number_input("Workshop Seat Price ($)", value=25.00, step=1.00)
    no_show_rate = st.slider("No-Show Rate (%)", 0, 100, 0) / 100.0
    extra_expenses = st.number_input("Extra Manual Expenses (e.g. Marketing)", value=0.00, step=10.00)

    if st.button("Simulate Month"):
        # 1. Demand Math: q(p) = max(0, 160 - 3.2p)
        requested = math.floor(max(0, 160 - 3.2 * price))

        # 2. Capacity Constraints
        staff_hours = 30
        hours_per_unit = 0.5
        venue_seats = 60
        max_capacity = min(math.floor(staff_hours / hours_per_unit), venue_seats)

        # 3. Fulfillment Math
        booked = min(requested, max_capacity)
        attended = math.floor(booked * (1 - no_show_rate))

        # 4. Financial Calculations
        revenue = attended * price
        variable_costs = attended * 5.00  # $2 educator + $2 materials + $1 cleaning
        fixed_costs = 700.00  # $250 venue + $100 software + $200 access + $150 admin
        total_costs = variable_costs + fixed_costs + extra_expenses
        profit = revenue - total_costs

        # 5. Ledger Updates
        date_str = st.session_state.current_date.strftime('%Y-%m-%d')
        st.session_state.ledger.append({"date": date_str, "description": f"Workshop Revenue ({attended} attended)", "category": "Revenue", "amount": revenue})
        st.session_state.ledger.append({"date": date_str, "description": "Variable Costs (Educator/Mat/Clean)", "category": "Variable Cost", "amount": -variable_costs})
        st.session_state.ledger.append({"date": date_str, "description": "Fixed Costs (Venue/Soft/Access/Admin)", "category": "Fixed Cost", "amount": -fixed_costs})

        if extra_expenses > 0:
            st.session_state.ledger.append({"date": date_str, "description": "Manual/Extra Expenses", "category": "Operating Expense", "amount": -extra_expenses})

        # 6. State Updates
        st.session_state.cash += profit
        st.session_state.retained_earnings += profit

        # Save results so they survive the rerun
        st.session_state.last_result = {
            "booked": booked, "attended": attended,
            "revenue": revenue, "costs": total_costs, "profit": profit
        }

        # Advance Date
        st.session_state.current_date += relativedelta(months=1)
        st.session_state.month_index += 1
        st.rerun()

    # Show last month's results (persisted across st.rerun())
    r = st.session_state.last_result
    if r:
        st.success(f"Month completed! Booked: {r['booked']} | Attended: {r['attended']}")
        st.info(f"Revenue: ${r['revenue']:,.2f} | Costs: ${r['costs']:,.2f} | Profit: ${r['profit']:,.2f}")

with tab2:
    st.header("Financial Ledger")
    df_ledger = pd.DataFrame(st.session_state.ledger)
    st.dataframe(df_ledger, use_container_width=True)

    st.subheader("State Save/Load")
    # Allows students to export their JSON snapshot for the AI Assistants
    state_json = json.dumps({
        "date": st.session_state.current_date.strftime('%Y-%m-%d'),
        "cash": st.session_state.cash,
        "ledger": st.session_state.ledger
    }, indent=2)
    st.download_button("Download JSON Snapshot", data=state_json, file_name="nur2_snapshot.json")

with tab3:
    st.header("Precalculus Data Models")
    st.markdown("### Average Cost Function")
    st.latex(r"A(s) = \frac{700}{s} + 5")
    st.caption("Vertical asymptote at s=0, Horizontal asymptote at y=5 (as seats approach infinity, average cost approaches the $5 variable cost).")

    st.markdown("### Applied Demand & Revenue")
    st.latex(r"q(p) = \max(0, 160 - 3.2p)")
    st.latex(r"R(p) = p \cdot \min(60, q(p))")

    st.markdown("### Advanced Seasonal Extension")
    st.latex(r"D(t) = 80\left(1 + 0.20\sin\left(\frac{2\pi(t-1)}{12}\right)\right)")
    st.caption("Trigonometric demand variation peaking at t=4 (Spring) and dipping at t=10 (Fall).")
