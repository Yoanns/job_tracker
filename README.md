# Job Application Tracker

A simple and intuitive Streamlit web application for tracking job applications. This tool helps job seekers organize their applications, monitor progress, and analyze their job search statistics.

## Features

- **Quick Add Form**: Guided form-based entry for new job applications with validation
- **Interactive Data Editor**: Spreadsheet-like interface for viewing and editing applications
- **Pagination Support**: Navigate through large lists of applications with configurable items per page (5, 10, 20, 50, or 100)
- **Page Navigation**: Use Previous/Next buttons or jump directly to any page
- **Auto-Save**: Changes are saved with visual confirmation and timestamp
- **Smart Dropdowns**: Pre-defined options for source, status, and offer fields prevent data entry errors
- **Clickable Links**: Direct access to job postings from the application table
- **Date Pickers**: Native date selection for all date fields
- **Statistics Dashboard**: Track your application progress with customizable timeframes
- **Dual Format Storage**: Automatically saves data to both CSV and JSON formats
- **Auto Follow-up**: Automatically calculates follow-up dates 5 days after application
- **Input Validation**: Ensures required fields are filled before submission
- **Unsaved Changes Warning**: Visual indicator when you have unsaved edits

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/job-application-tracker.git
cd job-application-tracker
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Usage

### Viewing and Managing Applications

1. Navigate to the **"View / Edit"** tab to see all applications
2. **Pagination Controls**:
   - Use the "Items per page" dropdown at the top to select how many entries to display (5, 10, 20, 50, or 100)
   - Navigate between pages using the Previous (◀) and Next (▶) buttons
   - Jump to a specific page using the "Go to" number input
   - View current page information (e.g., "Page 1 of 5 (21 total)")
3. **Edit cells**: Click any cell to modify data directly
4. **Add rows**: Click the "+" icon at the bottom of the table
5. **Delete rows**: Select row checkboxes and press the Delete key
6. **Use dropdowns**: Click dropdown cells to select from predefined options
7. **Pick dates**: Click date cells to use the calendar picker
8. **Click links**: Job posting links are clickable directly in the table
9. Click **"💾 Save Changes"** to save your edits (button is disabled when there are no changes)
10. View the last save timestamp in the top-right corner

### Adding Applications

1. Navigate to the **"Add Entry"** tab
2. Fill in the required fields (Company, Position, Application Date)
3. Select options from dropdowns for Source, Status, and Offer status
4. Complete optional fields as needed (Link, Location, Interview Date, Notes)
5. Click **"Add Application"** - the entry is automatically saved

### Viewing Statistics

1. Go to the **"Statistics"** tab
2. Select a timeframe from the dropdown:
   - All Time
   - Last 7 Days
   - Last 4 Weeks
3. View real-time metrics:
   - Total applications submitted
   - Applications that reached interview stage
   - Applications awaiting response

## Data Storage

The application automatically creates and maintains two data files:

- `applications.csv` - Main data storage in CSV format
- `applications.json` - Backup data storage in JSON format

Both files are created automatically on first run and update in real-time as you make changes.

## Application Fields

| Field          | Type     | Required | Description                                        |
| -------------- | -------- | -------- | -------------------------------------------------- |
| Company        | Text     | Yes      | Name of the company                                |
| Position       | Text     | Yes      | Job title/position                                 |
| Link           | URL      | No       | Link to job posting                                |
| Location       | Text     | No       | City, Country                                      |
| Date Applied   | Date     | Yes      | When you submitted the application                 |
| Source         | Dropdown | Yes      | Where you found the job (LinkedIn, Indeed, etc.)   |
| Status         | Dropdown | Yes      | Current application status                         |
| Follow-up      | Date     | Auto     | Automatically set to 5 days after application date |
| Interview Date | Date     | No       | Scheduled interview date                           |
| Offer Received | Dropdown | Yes      | Not yet / Yes / No                                 |
| Notes          | Text     | No       | Additional notes or comments                       |

## Project Structure

```
job-application-tracker/
├── app.py              # Main application file with UI
├── tracker.py          # Backend logic and data management
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .gitignore         # Git ignore rules
├── applications.csv   # Generated data file (ignored by git)
└── applications.json  # Generated backup file (ignored by git)
```

## Technologies Used

- **Python 3**: Core programming language
- **Streamlit**: Web application framework with interactive widgets
- **CSV Module**: Data storage and processing
- **JSON Module**: Backup data format
- **Datetime**: Date handling and calculations

## Tips for Best Results

- Use the form in "Add Entry" for your first applications to get familiar with the fields
- Use the data editor in "View / Edit" for quick updates to existing entries
- Adjust "Items per page" to suit your screen size and number of applications
- Use pagination to keep the interface clean and performant with many entries
- Review the "Statistics" tab regularly to monitor your job search progress
- Use the Notes field to track important details like recruiter names or salary ranges
- Update Status regularly to keep your pipeline accurate
- Always save your changes before navigating to a different page or tab

## Key Features Explained

### Pagination

The pagination system helps manage large numbers of applications efficiently:

- Choose your preferred page size from 5 to 100 items
- Navigation controls remain at the bottom for easy access
- Page state persists as you edit entries
- Automatic page adjustment when deleting entries

### Session State Management

The application uses Streamlit's session state to:

- Maintain your current page position
- Cache edited data before saving
- Track unsaved changes with visual warnings
- Remember your pagination preferences

## Contributing

This is a student project created for a Python Basics course. Feel free to fork and improve upon the code for your own learning purposes.

## License

This project is open source and available under the MIT License.
