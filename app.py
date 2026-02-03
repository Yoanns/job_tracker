import streamlit as st
import tracker as tr
from datetime import date, timedelta, datetime
import time


# Main App
st.set_page_config(page_title="Job Applications Tracker", page_icon="📋", layout="wide")
st.title("Job Application Tracker")

applications = tr.load_data()

tab1, tab2, tab3 = st.tabs(["View / Edit", "Add Entry", "Statistics"])

with tab1:
    st.header("Manage Applications")
    applications = tr.load_data()  # list[dict]

    if not applications:
        st.info(
            "No applications found. Add your first application in the 'Add Entry' tab!"
        )
    else:
        # Initialize session state
        if "editor_data" not in st.session_state:
            st.session_state.editor_data = applications
        if "last_save_time" not in st.session_state:
            st.session_state.last_save_time = None
        if "current_page" not in st.session_state:
            st.session_state.current_page = 1
        if "items_per_page" not in st.session_state:
            st.session_state.items_per_page = 10

        # Pagination controls
        col_selector, col_spacer = st.columns([1, 4])
        with col_selector:
            items_per_page = st.selectbox(
                "Items per page",
                options=[5, 9, 15, 30, 50],
                index=1,
                key="items_per_page_selector",
            )
            st.session_state.items_per_page = items_per_page

        # Calculate pagination
        total_items = len(st.session_state.editor_data)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        total_pages = max(1, total_pages)  # At least 1 page

        # Ensure current page is valid
        if st.session_state.current_page > total_pages:
            st.session_state.current_page = total_pages

        # Calculate slice indices
        start_idx = (st.session_state.current_page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)

        # Get current page data
        current_page_data = st.session_state.editor_data[start_idx:end_idx]

        # Info and timestamp
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(
                "Edit inline. Add rows with ‘+’. Delete rows via checkboxes + Delete key."
            )
        with col2:
            if st.session_state.last_save_time:
                st.caption(f"Last saved: {st.session_state.last_save_time}")

        # Placeholders
        save_placeholder = st.empty()
        warn_placeholder = st.empty()

        # Display editable table with paginated data
        edited_page = st.data_editor(
            current_page_data,
            num_rows="dynamic",
            width="stretch",
            key=f"data_editor_page_{st.session_state.current_page}",
            column_config={
                "company": st.column_config.TextColumn("Company", required=True),
                "position": st.column_config.TextColumn("Position", required=True),
                "link": st.column_config.LinkColumn("Job Link"),
                "location": st.column_config.TextColumn("Location"),
                "date_applied": st.column_config.DateColumn(
                    "Applied", format="YYYY-MM-DD", required=True
                ),
                "source": st.column_config.SelectboxColumn(
                    "Source", options=tr.SOURCES, required=True
                ),
                "status": st.column_config.SelectboxColumn(
                    "Status", options=tr.STATUS_OPTIONS, required=True
                ),
                "follow_up": st.column_config.DateColumn(
                    "Follow-up", format="YYYY-MM-DD"
                ),
                "interview_date": st.column_config.DateColumn(
                    "Interview", format="YYYY-MM-DD"
                ),
                "offer_received": st.column_config.SelectboxColumn(
                    "Offer", options=tr.OFFER_OPTIONS, required=True
                ),
                "notes": st.column_config.TextColumn("Notes"),
            },
        )

        # Merge edited page data back into full dataset
        updated_data = st.session_state.editor_data.copy()
        updated_data[start_idx:end_idx] = edited_page

        # Detect changes
        has_changes = updated_data != st.session_state.editor_data

        # Warning if unsaved edits
        if has_changes:
            warn_placeholder.warning("You have unsaved changes")
        else:
            warn_placeholder.empty()

        # Save button
        if st.button("💾 Save Changes", disabled=not has_changes, width="stretch"):
            tr.save_data(updated_data)  # write list-of-dicts to CSV/JSON
            st.session_state.editor_data = updated_data  # update cache
            st.session_state.last_save_time = datetime.now().strftime("%H:%M:%S")
            # st.success("✅ Changes saved!")

            # Clear warning
            warn_placeholder.empty()

            # Show success for 2 seconds
            save_placeholder.success("✅ Changes saved!")
            time.sleep(3)
            save_placeholder.empty()
            st.rerun()

        # BOTTOM ROW: Navigation controls
        st.divider()
        col_prev, col_goto, col_info, col_next = st.columns([1, 1, 2, 1])

        with col_prev:
            with col_prev:
                if st.button("◀ Previous", disabled=st.session_state.current_page == 1, width="stretch"):
                    st.session_state.current_page = max(1, st.session_state.current_page - 1)
                    st.rerun()

            with col_goto:
                page_input = st.number_input(
                    "Go to",
                    min_value=1,
                    max_value=total_pages,
                    value=st.session_state.current_page,
                    key="page_goto",
                )
                if page_input != st.session_state.current_page:
                    st.session_state.current_page = page_input
                    st.rerun()

            with col_info:
                # st.write(
                #     f"Page {st.session_state.current_page} of {total_pages} ({total_items} total)"
                # )
                st.markdown(
                    f"<div style='text-align: center; padding-top: 8px;'>Page {st.session_state.current_page} of {total_pages} ({total_items} total)</div>",
                    unsafe_allow_html=True,
                )
            with col_next:
                if st.button(
                    "Next ▶", disabled=st.session_state.current_page >= total_pages
                ):
                    st.session_state.current_page = min(
                        total_pages, st.session_state.current_page + 1
                    )
                    st.rerun()


with tab2:
    st.header("Add New Application")
    with st.form("add_form", clear_on_submit=True):
        company = st.text_input(
            "Company *", placeholder="Enter company name", key="company"
        )
        position = st.text_input(
            "Position *", placeholder="Enter job position", key="position"
        )
        link = st.text_input(
            "Link to Job Description", placeholder="https://...", key="link"
        )
        location = st.text_input(
            "Location", placeholder="City, Country", key="location"
        )
        date_applied = st.date_input("Date Applied *", date.today(), key="date_applied")
        source = st.selectbox("Source", tr.SOURCES, key="source")
        status = st.selectbox("Status", tr.STATUS_OPTIONS, key="status")
        follow_up = date_applied + timedelta(days=5)
        st.write(f"Follow-Up Date (auto): {follow_up}")
        interview_date = st.date_input("Interview Date", None, key="interview_date")
        offer_received = st.selectbox(
            "Offer Received", tr.OFFER_OPTIONS, key="offer_received"
        )
        notes = st.text_area("Notes", placeholder="Additional notes...", key="notes")

        submitted = st.form_submit_button("Add Application")
        save_placeholder = st.empty()

        if submitted:
            validation_errors = tr.validate_entry(company, position, date_applied)

            if validation_errors:
                for error in validation_errors:
                    st.error(error)
            else:
                entry = {
                    "company": company,
                    "position": position,
                    "link": link,
                    "location": location,
                    "date_applied": date_applied.strftime("%Y-%m-%d"),
                    "source": source,
                    "status": status,
                    "follow_up": follow_up.strftime("%Y-%m-%d"),
                    "interview_date": (
                        interview_date.strftime("%Y-%m-%d") if interview_date else ""
                    ),
                    "offer_received": offer_received,
                    "notes": notes,
                }

                applications.append(entry)
                tr.save_data(applications)
                if "editor_data" in st.session_state:
                    del st.session_state["editor_data"]

                save_placeholder.success("✅ Application added successfully!")
                time.sleep(3)
                save_placeholder.empty()

with tab3:
    st.header("Statistics")
    if applications:
        timeframe = st.selectbox(
            "Time Frame", ["All Time", "Last 7 Days", "Last 4 Weeks"]
        )

        days = None
        if timeframe == "Last 7 Days":
            days = 7
        elif timeframe == "Last 4 Weeks":
            days = 28

        total, interviewed, awaiting = tr.compute_stats(applications, days)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Applications", total)
        with col2:
            st.metric("Interviewed", interviewed)
        with col3:
            st.metric("Awaiting Response", awaiting)
    else:
        st.info("No data available for statistics. Add some applications first!")
