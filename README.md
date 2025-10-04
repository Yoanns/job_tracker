# Job Application Tracker

A simple and intuitive Streamlit web application for tracking job applications. Built as a Python Basics course project, this tool helps job seekers organize their applications, monitor progress, and analyze their job search statistics.

## Features

- **Quick Add Form**: Guided form-based entry for new job applications with validation
- **Interactive Data Editor**: Spreadsheet-like interface for viewing and editing applications
- **Auto-Save**: Changes are saved automatically with visual confirmation
- **Smart Dropdowns**: Pre-defined options for source, status, and offer fields prevent data entry errors
- **Clickable Links**: Direct access to job postings from the application table
- **Date Pickers**: Native date selection for all date fields
- **Statistics Dashboard**: Track your application progress with customizable timeframes
- **Dual Format Storage**: Automatically saves data to both CSV and JSON formats
- **Auto Follow-up**: Automatically calculates follow-up dates 5 days after application
- **Input Validation**: Ensures required fields are filled before submission

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/job-application-tracker.git
cd job-application-tracker
```

2. Install required dependencies:

```
pip install -r requirements.txt
```

### Running the Application

Start the Streamlit app:

```
streamlit run tracker.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Usage

### Adding Applications

1. Navigate to the "Add Entry" tab
2. Fill in the required fields (Company, Position, Application Date)
3. Select options from dropdowns for Source, Status, and Offer status
4. Complete optional fields as needed (Link, Location, Interview Date, Notes)
5. Click "Add Application" - the entry is automatically saved

### Managing Applications

1. Use the "Manage Applications" tab to see all applications in an editable table
2. **Edit cells**: Click any cell to modify data directly
3. **Add rows**: Click the "+" icon at the bottom of the table
4. **Delete rows**: Select row checkboxes and press the Delete key
5. **Use dropdowns**: Click dropdown cells to select from predefined options
6. **Pick dates**: Click date cells to use the calendar picker
7. **Click links**: Job posting links are clickable directly in the table
8. Changes save automatically with timestamp confirmation

### Viewing Statistics

1. Go to the "Statistics" tab
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
├── tracker.py          # Main application file
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
- Use the data editor in "Manage Applications" for quick updates to existing entries
- Review the "Statistics" tab regularly to monitor your job search progress
- Use the Notes field to track important details like recruiter names or salary ranges
- Update Status regularly to keep your pipeline accurate

## Contributing

This is a student project created for a Python Basics course. Feel free to fork and improve upon the code for your own learning purposes.

## License

This project is open source and available under the MIT License.
