
import streamlit as st
import json
import os

DATA_FILE = "web_budget_data.json"

# Load budget data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"allowance": 0, "saved": 0}

# Save budget data to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Set page config
st.set_page_config(page_title="Budget Tracker", layout="centered")
st.markdown("<h1 style='text-align: center;'>📊 Monthly Budget Tracker</h1>", unsafe_allow_html=True)

# Load or initialize data
data = load_data()

# Input for monthly allowance
st.subheader("Set Your Monthly Allowance")
allowance = st.number_input("Monthly Allowance (R)", min_value=0.0, step=100.0, value=float(data["allowance"]))
data["allowance"] = allowance

if allowance > 0:
    suggested_save = allowance * 0.20
    suggested_spend = allowance * 0.80

    st.success(f"💡 Suggested Budget: Save R{suggested_save:.2f}, Spend R{suggested_spend:.2f}")

    # Input for savings
    st.subheader("Add to Savings")
    save_input = st.number_input("Add Savings Amount (R)", min_value=0.0, step=50.0)

    if st.button("Add Savings"):
        data["saved"] += save_input
        st.success(f"✅ Added R{save_input:.2f} to savings!")

    # Show savings progress
    saved = data["saved"]
    savings_goal = allowance * 0.20
    percent = min(saved / savings_goal, 1.0)

    st.subheader("Progress Toward Savings Goal")
    st.progress(percent)
    st.metric(label="Total Saved", value=f"R{saved:.2f}")
    st.metric(label="Savings Goal", value=f"R{savings_goal:.2f}")
    st.metric(label="Remaining", value=f"R{max(0, savings_goal - saved):.2f}")

else:
    st.warning("Please set your monthly allowance above to get started.")

# Save updated data
save_data(data)
