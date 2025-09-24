# Job Application Tracker

A simple and intuitive Streamlit web application for tracking job applications. Built as a Python Basics course project, this tool helps job seekers organize their applications, monitor progress, and analyze their job search statistics.

## Features

- **Add Applications**: Easy form-based entry for new job applications
- **View & Edit**: Interactive data table for viewing and editing existing applications
- **Statistics Dashboard**: Track your application progress with metrics and timeframes
- **Data Persistence**: Automatically saves data to CSV and JSON formats
- **Auto Follow-up**: Automatically sets follow-up dates 5 days after application
- **Input Validation**: Ensures required fields are filled before submission

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
streamlit run tracker.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Usage

### Adding Applications

1. Navigate to the "Add Entry" tab
2. Fill in the required fields (Company, Position, Application Date)
3. Complete optional fields as needed
4. Click "Add Application" to save

### Managing Applications

1. Use the "View / Edit" tab to see all applications
2. Edit data directly in the table
3. Click "Save Changes" to persist modifications

### Viewing Statistics

1. Go to the "Statistics" tab
2. Select a timeframe (All Time, Last 7 Days, Last 4 Weeks)
3. View metrics for total applications, interviews, and pending responses
4. Use "Refresh Statistics" to update the data

## Data Storage

The application automatically creates and maintains two data files:

- `applications.csv` - Main data storage in CSV format
- `applications.json` - Backup data storage in JSON format

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
- **Streamlit**: Web application framework
- **CSV**: Data storage and processing
- **JSON**: Backup data format

## Contributing

This is a student project created for a Python Basics course. Feel free to fork and improve upon the code for your own learning purposes.

## License

This project is open source and available under the MIT License.
