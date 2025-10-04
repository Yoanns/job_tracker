import time
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
EMPTY_FORM = {
    'company': '',
    'position': '',
    'link': '',
    'location': '',
    'date_applied': date.today(),
    'source': SOURCES[0],
    'status': STATUS_OPTIONS[0],
    'follow_up': date.today() + timedelta(days=5),
    'interview_date': None,
    'offer_received': OFFER_OPTIONS[0],
    'notes': ''
}

def ensure_files():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()

    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w') as f:
            json.dump([], f, indent=2)

# def load_data():
#     ensure_files()
#     try:
#         with open(CSV_FILE, 'r', newline='') as f:
#             reader = csv.DictReader(f)
#             return list(reader)
#     except Exception as e:
#         st.error(f"Error loading  {e}")
#         return []

# def save_data(data):
#     try:
#         with open(CSV_FILE, 'w', newline='') as f:
#             writer = csv.DictWriter(f, fieldnames=FIELDS)
#             writer.writeheader()
#             writer.writerows(data)

#         with open(JSON_FILE, 'w') as f:
#             json.dump(data, f, indent=2)
#     except Exception as e:
#         st.error(f"Error saving  {e}")

def load_data():
    ensure_files()
    try:
        with open(CSV_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        # Convert string dates to date objects for data_editor compatibility
        for entry in data:
            # Convert date_applied
            if entry['date_applied']:
                try:
                    entry['date_applied'] = datetime.strptime(entry['date_applied'], '%Y-%m-%d').date()
                except ValueError:
                    entry['date_applied'] = None
            else:
                entry['date_applied'] = None

            # Convert follow_up
            if entry['follow_up']:
                try:
                    entry['follow_up'] = datetime.strptime(entry['follow_up'], '%Y-%m-%d').date()
                except ValueError:
                    entry['follow_up'] = None
            else:
                entry['follow_up'] = None

            # Convert interview_date
            if entry['interview_date']:
                try:
                    entry['interview_date'] = datetime.strptime(entry['interview_date'], '%Y-%m-%d').date()
                except ValueError:
                    entry['interview_date'] = None
            else:
                entry['interview_date'] = None

        return data
    except Exception as e:
        st.error(f"Error loading  {e}")
        return []

def save_data(data):
    try:
        # Convert date objects back to strings for CSV storage
        data_to_save = []
        for entry in data:
            entry_copy = entry.copy()

            # Convert date_applied
            if isinstance(entry_copy['date_applied'], date):
                entry_copy['date_applied'] = entry_copy['date_applied'].strftime('%Y-%m-%d')
            elif not entry_copy['date_applied']:
                entry_copy['date_applied'] = ''

            # Convert follow_up
            if isinstance(entry_copy['follow_up'], date):
                entry_copy['follow_up'] = entry_copy['follow_up'].strftime('%Y-%m-%d')
            elif not entry_copy['follow_up']:
                entry_copy['follow_up'] = ''

            # Convert interview_date
            if isinstance(entry_copy['interview_date'], date):
                entry_copy['interview_date'] = entry_copy['interview_date'].strftime('%Y-%m-%d')
            elif not entry_copy['interview_date']:
                entry_copy['interview_date'] = ''

            data_to_save.append(entry_copy)

        # Save to CSV
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(data_to_save)

        # Save to JSON
        with open(JSON_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=2)
    except Exception as e:
        st.error(f"Error saving  {e}")

def auto_save_with_feedback():
    """Save and show feedback"""
    try:
        if 'data_editor' in st.session_state:
            edited_data = st.session_state.data_editor
            save_data(edited_data)
            st.session_state.editor_data = edited_data
            st.session_state.last_save_time = datetime.now().strftime('%H:%M:%S')
            st.toast("✅ Saved", icon="✅")
    except Exception as e:
        st.toast(f"⚠️ Save failed: {e}", icon="⚠️")


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
                # Check if it's already a date object or needs conversion
                if isinstance(entry['date_applied'], date):
                    applied = entry['date_applied']
                elif isinstance(entry['date_applied'], str):
                    applied = datetime.strptime(entry['date_applied'], '%Y-%m-%d').date()
                else:
                    continue

                if timeframe_days is None or (today - applied).days <= timeframe_days:
                    filtered.append(entry)
        except (ValueError, TypeError):
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
        # Initialize data
        if 'editor_data' not in st.session_state:
            st.session_state.editor_data = applications
        if 'last_save_time' not in st.session_state:
            st.session_state.last_save_time = None

        # Show last save time
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("💡 Changes save automatically. Delete rows with Delete key, add with '+'")
        with col2:
            if st.session_state.last_save_time:
                st.caption(f"Last saved: {st.session_state.last_save_time}")

        # Data editor with auto-save
        edited = st.data_editor(
            st.session_state.editor_data,
            num_rows='dynamic',
            width="stretch",
            key='data_editor',
            on_change=auto_save_with_feedback,
            column_config={
                "source": st.column_config.SelectboxColumn(
                    "Source",
                    help="Where did you find this job?",
                    width="medium",
                    options=SOURCES,
                    required=True
                ),
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    help="Current application status",
                    width="medium",
                    default="Applied",
                    options=STATUS_OPTIONS,
                    required=True
                ),
                "offer_received": st.column_config.SelectboxColumn(
                    "Offer",
                    help="Have you received an offer?",
                    width="small",
                    options=OFFER_OPTIONS,
                    required=True
                ),
                "link": st.column_config.LinkColumn(
                    "Job Link",
                    help="Link to job posting",
                    width="medium"
                ),
                "date_applied": st.column_config.DateColumn(
                    "Applied",
                    help="Date application was submitted",
                    width="medium",
                    format="YYYY-MM-DD",
                    required=True
                ),
                "follow_up": st.column_config.DateColumn(
                    "Follow-up",
                    help="Recommended follow-up date",
                    width="medium",
                    format="YYYY-MM-DD"
                ),
                "interview_date": st.column_config.DateColumn(
                    "Interview",
                    help="Scheduled interview date",
                    width="medium",
                    format="YYYY-MM-DD"
                ),
            }
        )

        st.session_state.editor_data = edited
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
