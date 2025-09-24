import streamlit as st
import csv
import os
import json
from datetime import datetime, date, timedelta

# Constants
CSV_FILE = 'applications.csv'
JSON_FILE = 'applications.json'
FIELDS = ['company', 'position', 'link', 'location', 'date_applied', 'source', 'status', 'follow_up', 'interview_date', 'offer_received', 'notes']
SOURCES = ['Website', 'LinkedIn', 'Xing', 'Indeed', 'Online Search', 'Referral', 'Other']
STATUS_OPTIONS = ['Applied', 'Phone Screen', 'Interview Scheduled', 'Offer', 'Rejected', 'Withdrawn']
OFFER_OPTIONS = ['Not yet', 'Yes', 'No']

def ensure_files():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()

    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w') as f:
            json.dump([], f, indent=2)

def load_data():
    ensure_files()
    try:
        with open(CSV_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        st.error(f"Error loading  {e}")
        return []

def save_data(data):
    try:
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(data)

        with open(JSON_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving  {e}")

def validate_entry(company, position, date_applied):
    errors = []
    if not company.strip():
        errors.append("Company name is required")
    if not position.strip():
        errors.append("Position is required")
    if not date_applied:
        errors.append("Application date is required")
    return errors

def compute_stats(data, timeframe_days=None):
    filtered = []
    today = date.today()

    for entry in data:
        try:
            if entry['date_applied']:
                applied = datetime.strptime(entry['date_applied'], '%Y-%m-%d').date()
                if timeframe_days is None or (today - applied).days <= timeframe_days:
                    filtered.append(entry)
        except ValueError:
            continue

    total = len(filtered)
    interviewed = sum(1 for e in filtered if e['status'] in ['Phone Screen', 'Interview Scheduled', 'Offer'])
    awaiting = sum(1 for e in filtered if e['status'] == 'Applied')

    return total, interviewed, awaiting

# Main App
st.set_page_config(page_title="Job Applications Tracker", page_icon="📋", layout="centered")
st.title('Job Application Tracker')

applications = load_data()

tab1, tab2, tab3 = st.tabs(['View / Edit', 'Add Entry', 'Statistics'])

with tab1:
    st.header('Current Applications')
    if applications:
        edited = st.data_editor(applications, num_rows='dynamic', width='stretch')
        if st.button('Save Changes'):
            save_data(edited)
            st.success('Changes saved successfully!')
    else:
        st.info("No applications found. Add your first application in the 'Add Entry' tab!")

with tab2:
    st.header('Add New Application')
    with st.form('add_form', clear_on_submit=True):
        company = st.text_input('Company *', placeholder="Enter company name",key='company')
        position = st.text_input('Position *', placeholder="Enter job position", key='position')
        link = st.text_input('Link to Job Description', placeholder="https://...", key='link')
        location = st.text_input('Location', placeholder="City, Country", key='location')
        date_applied = st.date_input('Date Applied *', date.today(), key='date_applied')
        source = st.selectbox('Source', SOURCES, key='source')
        status = st.selectbox('Status', STATUS_OPTIONS, key='status')
        follow_up = date_applied + timedelta(days=5)
        st.write(f"Follow-Up Date (auto): {follow_up}")
        interview_date = st.date_input('Interview Date', None, key='interview_date')
        offer_received = st.selectbox('Offer Received', OFFER_OPTIONS, key='offer_received')
        notes = st.text_area('Notes', placeholder="Additional notes...", key='notes')

        submitted = st.form_submit_button('Add Application')

        if submitted:
            validation_errors = validate_entry(company, position, date_applied)

            if validation_errors:
                for error in validation_errors:
                    st.error(error)
            else:
                entry = {
                    'company': company,
                    'position': position,
                    'link': link,
                    'location': location,
                    'date_applied': date_applied.strftime('%Y-%m-%d'),
                    'source': source,
                    'status': status,
                    'follow_up': follow_up.strftime('%Y-%m-%d'),
                    'interview_date': interview_date.strftime('%Y-%m-%d') if interview_date else '',
                    'offer_received': offer_received,
                    'notes': notes
                }

                applications.append(entry)
                save_data(applications)
                st.success('Application added successfully!')

with tab3:
    st.header('Statistics')
    if applications:
        # Refresh button
        if st.button('Refresh Statistics'):
            # Rerun to refresh stats
            total, interviewed, awaiting = compute_stats(applications, None)
        timeframe = st.selectbox('Time Frame', ['All Time', 'Last 7 Days', 'Last 4 Weeks'])

        days = None
        if timeframe == 'Last 7 Days':
            days = 7
        elif timeframe == 'Last 4 Weeks':
            days = 28

        total, interviewed, awaiting = compute_stats(applications, days)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Total Applications', total)
        with col2:
            st.metric('Interviewed', interviewed)
        with col3:
            st.metric('Awaiting Response', awaiting)
    else:
        st.info("No data available for statistics. Add some applications first!")
