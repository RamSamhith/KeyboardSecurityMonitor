"""
Helper Utilities Module
Contains utility functions for the application
"""

import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

def format_duration(seconds: int) -> str:
    """Format seconds into HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def calculate_wpm(total_chars: int, duration_seconds: int) -> float:
    """Calculate words per minute"""
    if duration_seconds <= 0:
        return 0.0
    minutes = duration_seconds / 60
    words = total_chars / 5  # Standard: 5 characters = 1 word
    return round(words / minutes, 2)

def calculate_accuracy(correct_chars: int, total_chars: int) -> float:
    """Calculate accuracy percentage"""
    if total_chars <= 0:
        return 0.0
    return round((correct_chars / total_chars) * 100, 2)

def get_key_frequency(keys_pressed: List[str]) -> Dict[str, int]:
    """Calculate frequency of each key pressed"""
    frequency = {}
    for key in keys_pressed:
        if key in frequency:
            frequency[key] += 1
        else:
            frequency[key] = 1
    return frequency

def get_timestamp() -> str:
    """Get current timestamp as string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sanitize_text(text: str) -> str:
    """Sanitize text input"""
    return text.strip()
