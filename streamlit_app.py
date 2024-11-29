import streamlit as st

# Title of the dashboard
st.title("📊 Interactive Formula-Based Dashboard")

# Description
st.write(
    "This dashboard allows you to choose values from dropdown menus, calculates a formula "
    "based on the selected inputs, and displays different outputs depending on the result."
)

# Define the dropdown options for the user
option1_values = [10, 20, 30, 40, 50]  # Example values for Option 1
option2_values = [5, 15, 25, 35, 45]   # Example values for Option 2
option3_values = [1, 2, 3, 4, 5]       # Example values for Option 3

# Sidebar for user input
st.sidebar.header("Input Parameters")
option1 = st.sidebar.selectbox("Select Value for Option 1", option1_values)
option2 = st.sidebar.selectbox("Select Value for Option 2", option2_values)
option3 = st.sidebar.selectbox("Select Value for Option 3", option3_values)

# Formula to calculate the output based on selected inputs
# Example formula: (option1 + option2) * option3
formula_result = (option1 + option2) * option3

# Display the formula and result
st.write("### Formula Calculation")
st.write(f"Formula: `(Option 1 + Option 2) * Option 3`")
st.write(f"Result: `{formula_result}`")

# Conditional outputs based on the formula result
st.write("### Result Analysis")
if formula_result < 100:
    st.success("The result is less than 100. Everything looks good!")
elif 100 <= formula_result < 200:
    st.warning("The result is between 100 and 200. Be cautious!")
else:
    st.error("The result is greater than 200. Immediate action is needed!")

# Debugging or optional detailed output
with st.expander("Detailed Inputs and Calculations"):
    st.write(f"Option 1 Selected: `{option1}`")
    st.write(f"Option 2 Selected: `{option2}`")
    st.write(f"Option 3
