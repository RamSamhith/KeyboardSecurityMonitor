"""
Configuration Module for Keyboard Security Monitor
Centralizes all application settings and constants
"""

import os
from pathlib import Path

# Application metadata
APP_NAME = "Keyboard Security Monitor"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Cybersecurity Intern"
APP_DESCRIPTION = "Educational typing security monitoring tool for cybersecurity students"

# Base paths
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
DATABASE_DIR = BASE_DIR / "database"
DOCS_DIR = BASE_DIR / "docs"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
UI_DIR = BASE_DIR / "ui"
UTILS_DIR = BASE_DIR / "utils"

# Database settings
DATABASE_NAME = "keyboard_monitor.db"
DATABASE_PATH = DATABASE_DIR / DATABASE_NAME

# Report settings
REPORTS_FORMAT = "pdf"
SAMPLE_DATA_COUNT = 50

# UI Settings
THEME = "dark"
COLORS = {
    "primary": "#1f538d",
    "secondary": "#4d90fe",
    "success": "#28a745",
    "warning": "#ffc107",
    "danger": "#dc3545",
    "background": "#1a1a2e",
    "surface": "#16213e",
    "text": "#ffffff",
    "text_secondary": "#a0a0a0"
}

# Typing test settings
TYPING_TEXTS = [
    "The quick brown fox jumps over the lazy dog",
    "Pack my box with five dozen liquor jugs",
    "How vexingly quick daft zebras jump",
    "The five boxing wizards jump quickly",
    "Jackdaws love my big sphinx of quartz"
]

# Logging settings
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "app.log"

# Create directories if they don't exist
for directory in [ASSETS_DIR, DATABASE_DIR, DOCS_DIR, MODELS_DIR, 
                  REPORTS_DIR, SCREENSHOTS_DIR, UI_DIR, UTILS_DIR]:
    directory.mkdir(exist_ok=True)
