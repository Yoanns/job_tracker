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
    'follow_up': date.today() + timedelta(days=21), # Default follow-up in 3 weeks
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
