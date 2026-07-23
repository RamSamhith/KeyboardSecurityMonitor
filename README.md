# Keyboard Security Monitor

An educational cybersecurity desktop application for learning about keyboard input monitoring and typing pattern analysis. Built as an internship-level project for cybersecurity students.

This project demonstrates defensive security concepts including input monitoring (within the application only), data collection, pattern analysis, and secure coding practices.

> This application only processes input within its own interface. It does not capture system-wide keystrokes or run in the background.

## Features

- Real-time WPM (Words Per Minute) calculation
- Typing accuracy tracking with live feedback
- Key frequency analysis within the typing area
- Session timer with automatic duration tracking
- Session history stored in SQLite database
- PDF report generation for completed sessions
- Searchable session history with delete functionality
- Dark/Light theme toggle
- Database export and import for backup
- Educational cybersecurity tips
- Responsive UI built with CustomTkinter

## Project Structure

The application follows a modular architecture with clear separation of concerns:

```
KeyboardSecurityMoniter/
├── app.py                  # Application entry point
├── config.py               # Configuration and constants
├── requirements.txt        # Python dependencies
├── database/
│   └── db_manager.py       # SQLite CRUD operations
├── models/
│   └── typing_model.py     # Data models for sessions
├── reports/
│   └── pdf_generator.py    # PDF report generation
├── ui/
│   ├── main_window.py      # Main window and navigation
│   ├── dashboard.py        # Statistics overview
│   ├── typing_page.py      # Typing practice area
│   ├── statistics_page.py  # Session history
│   ├── reports_page.py     # Report generation UI
│   ├── settings_page.py    # Application settings
│   └── about_page.py       # About and security tips
└── utils/
    ├── helpers.py           # Calculation utilities
    ├── charts.py            # Matplotlib chart functions
    └── security_tips.py     # Educational content
```

## Installation

### Prerequisites

- Python 3.12 or higher
- pip package manager
- Windows OS (primary platform)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/keyboard-security-monitor.git
cd keyboard-security-monitor

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Dependencies

The following packages will be installed automatically:

- `customtkinter` - Modern UI framework
- `matplotlib` - Chart generation
- `reportlab` - PDF report creation
- `Pillow` - Image processing support

## Usage

1. Launch the application with `python app.py`
2. Click **Typing Practice** in the sidebar
3. Click **Start New Session** and type the displayed text
4. Click **Stop & Save** to save your session to the database
5. View your statistics on the **Dashboard** or **Statistics** page
6. Generate PDF reports from the **Reports** page
7. Toggle theme and manage data in **Settings**

### Pages

- **Dashboard** - Overview of typing statistics, quick actions, and recent activity
- **Typing Practice** - Interactive typing area with real-time WPM and accuracy
- **Statistics** - Browse, search, and manage session history with checkboxes
- **Reports** - Generate single session or summary PDF reports
- **Settings** - Theme options, database export/import, reset all data
- **About** - Application information and educational security tips

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.12 | Core language and application logic |
| CustomTkinter | Modern, responsive UI framework |
| SQLite | Lightweight local database storage |
| Matplotlib | Performance charts and data visualization |
| ReportLab | Professional PDF report generation |

## Future Enhancements

- Real-time updating charts during typing sessions
- Achievement badges for typing milestones
- Multi-user profile support
- Custom typing practice texts
- CSV/JSON data export options
- Long-term typing trend analysis
- Typing test modes with timed challenges
- Keyboard layout visualization

## Contributing

Contributions are welcome. Please fork the repository and create a pull request with your changes.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**Cybersecurity Intern**

- GitHub:https://github.com/RamSamhith/KeyboardSecurityMonitor
