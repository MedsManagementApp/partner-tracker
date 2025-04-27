import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Initialize session state if not already done
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        'Partner Name', 'Last Meeting', 'Next Follow-up', 'Lead Status', 'Notes'
    ])

st.title("Partner Management Tracker")

# --- Form to add a new partner record ---
st.subheader("Add New Partner Update")
with st.form("new_partner"):
    partner_name = st.text_input("Partner Name")
    last_meeting = st.date_input("Last Meeting Date", value=datetime.today())
    next_followup = st.date_input("Next Follow-Up Date", value=datetime.today() + timedelta(days=30))
    lead_status = st.selectbox("Lead Status", ["New", "In Progress", "Closed", "No Response"])
    notes = st.text_area("Notes")
    submit = st.form_submit_button("Add Update")

if submit:
    new_row = {
        'Partner Name': partner_name,
        'Last Meeting': last_meeting,
        'Next Follow-up': next_followup,
        'Lead Status': lead_status,
        'Notes': notes
    }
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
    st.success("Update added successfully!")

# --- Display Current Partner Tracker ---
st.subheader("Current Partner Tracker")
st.dataframe(st.session_state.data)

# --- Optional: Filter by Lead Status ---
st.subheader("Filter by Lead Status")
selected_status = st.selectbox("Choose a status to filter", ["All"] + list(st.session_state.data['Lead Status'].unique()))

if selected_status != "All":
    filtered_data = st.session_state.data[st.session_state.data['Lead Status'] == selected_status]
else:
    filtered_data = st.session_state.data

st.dataframe(filtered_data)

# --- Download Option ---
st.subheader("Download Tracker Data")
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(st.session_state.data)

st.download_button(
    label="Download as CSV",
    data=csv,
    file_name='partner_tracker.csv',
    mime='text/csv',
)
