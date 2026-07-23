"""
Typing Model Module
Defines data structures for typing sessions
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

@dataclass
class TypingSession:
    """Represents a typing practice session"""
    id: int = None
    session_date: datetime = None
    duration_seconds: int = 0
    total_characters: int = 0
    correct_characters: int = 0
    wpm: float = 0.0
    accuracy: float = 0.0
    text_practiced: str = ""
    
    def calculate_wpm(self):
        """Calculate words per minute"""
        if self.duration_seconds > 0:
            minutes = self.duration_seconds / 60
            words = self.total_characters / 5  # Standard: 5 characters = 1 word
            self.wpm = round(words / minutes, 2)
        return self.wpm
        
    def calculate_accuracy(self):
        """Calculate typing accuracy percentage"""
        if self.total_characters > 0:
            self.accuracy = round((self.correct_characters / self.total_characters) * 100, 2)
        return self.accuracy
        
    def to_dict(self):
        """Convert session to dictionary"""
        return {
            'id': self.id,
            'session_date': self.session_date,
            'duration': self.duration_seconds,
            'total_chars': self.total_characters,
            'correct_chars': self.correct_characters,
            'wpm': self.wpm,
            'accuracy': self.accuracy,
            'text': self.text_practiced
        }

@dataclass
class KeyFrequency:
    """Represents frequency of a specific key"""
    key_char: str
    frequency: int = 0
    session_id: int = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'key_char': self.key_char,
            'frequency': self.frequency,
            'session_id': self.session_id
        }
