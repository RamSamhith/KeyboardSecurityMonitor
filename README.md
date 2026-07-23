# Keyboard Security Monitor

An educational cybersecurity desktop application for monitoring and analyzing keyboard typing patterns.

## Overview

This project is designed for cybersecurity students and interns to learn about:
- Keyboard input monitoring (within the application only)
- Typing pattern analysis
- Session tracking and reporting
- Data visualization

## Features

- Modern Dark Theme UI
- Real-time Typing Speed (WPM) Calculator
- Typing Accuracy Tracker
- Frequently Used Keys Analysis
- Session Timer
- Interactive Charts and Graphs
- PDF Report Generation
- SQLite Database Storage
- Educational Security Tips

## Installation

### Prerequisites

- Python 3.12 or higher
- pip package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/keyboard-security-monitor.git
   cd keyboard-security-monitor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Project Structure

```
keyboard-security-monitor/
├── assets/           # UI assets (icons, images)
├── database/         # SQLite database files
├── docs/            # Documentation
├── models/          # Data models
├── reports/         # Generated PDF reports
├── screenshots/     # Application screenshots
├── ui/              # UI components
├── utils/           # Utility functions
├── app.py           # Main application entry point
├── config.py        # Configuration settings
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Usage

1. Launch the application
2. Use the navigation menu to access different features
3. Practice typing in the Typing Practice Area
4. View your statistics on the Dashboard
5. Generate PDF reports from your typing sessions

## Educational Purpose

This application is designed for educational purposes only. It demonstrates:
- Input monitoring concepts (within the application scope)
- Data collection and analysis
- Pattern recognition
- Secure coding practices

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This application only processes input within its own interface. It does not
capture system-wide keystrokes or collect data without user consent.
