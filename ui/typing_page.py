"""
Typing Practice Page Module
Implements the typing practice functionality with database integration
"""

import time
import random
import logging
import customtkinter as ctk
from typing import List, Dict, Optional
from config import TYPING_TEXTS, COLORS
from database.db_manager import DatabaseManager
from utils.helpers import calculate_wpm, calculate_accuracy, format_duration

logger = logging.getLogger(__name__)


class TypingPage(ctk.CTkFrame):
    """Typing practice page with real-time statistics and session saving"""
    
    def __init__(self, parent, db_manager: DatabaseManager) -> None:
        super().__init__(parent, fg_color="transparent")
        
        # Database manager
        self.db = db_manager
        
        # Session variables
        self.start_time: Optional[float] = None
        self.is_typing: bool = False
        self.current_text: str = ""
        self.typed_text: str = ""
        self.keys_pressed: List[str] = []
        
        # UI elements
        self.create_widgets()
        
    def create_widgets(self) -> None:
        """Create page widgets"""
        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(self)
        scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            scrollable,
            text="⌨ Typing Practice",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(padx=20, pady=(10, 20), anchor="w")
        
        # Stats frame
        self.stats_frame = ctk.CTkFrame(scrollable)
        self.stats_frame.pack(fill="x", padx=10, pady=10)
        
        # WPM display
        self.wpm_label = ctk.CTkLabel(
            self.stats_frame,
            text="⚡ WPM: 0",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.wpm_label.pack(side="left", padx=20, pady=15)
        
        # Accuracy display
        self.accuracy_label = ctk.CTkLabel(
            self.stats_frame,
            text="✓ Accuracy: 100%",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.accuracy_label.pack(side="left", padx=20, pady=15)
        
        # Timer display
        self.timer_label = ctk.CTkLabel(
            self.stats_frame,
            text="⏱ Time: 00:00",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.timer_label.pack(side="left", padx=20, pady=15)
        
        # Characters count
        self.chars_label = ctk.CTkLabel(
            self.stats_frame,
            text="Chars: 0",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        self.chars_label.pack(side="right", padx=20, pady=15)
        
        # Reference text display
        ref_header = ctk.CTkLabel(
            scrollable,
            text="Type the following text:",
            font=ctk.CTkFont(size=13),
            text_color="gray60"
        )
        ref_header.pack(padx=20, pady=(10, 5), anchor="w")
        
        self.reference_frame = ctk.CTkFrame(scrollable, height=80)
        self.reference_frame.pack(fill="x", padx=10, pady=5)
        
        self.reference_label = ctk.CTkLabel(
            self.reference_frame,
            text="Click 'Start New Session' to begin typing practice",
            font=ctk.CTkFont(size=14),
            wraplength=900,
            justify="left"
        )
        self.reference_label.pack(expand=True, padx=15, pady=10)
        
        # Typing input area
        input_header = ctk.CTkLabel(
            scrollable,
            text="Your typing:",
            font=ctk.CTkFont(size=13),
            text_color="gray60"
        )
        input_header.pack(padx=20, pady=(10, 5), anchor="w")
        
        self.input_textbox = ctk.CTkTextbox(
            scrollable,
            height=120,
            font=ctk.CTkFont(size=14)
        )
        self.input_textbox.pack(fill="x", padx=10, pady=5)
        self.input_textbox.bind("<KeyRelease>", self.on_key_release)
        
        # Button frame
        self.button_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=10, pady=10)
        
        # Start button
        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="▶ Start New Session",
            command=self.start_typing,
            width=180,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.start_button.pack(side="left", padx=5)
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            self.button_frame,
            text="⏹ Stop & Save",
            command=self.stop_and_save,
            width=150,
            height=40,
            fg_color="#28a745",
            font=ctk.CTkFont(size=13),
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)
        
        # Reset button
        self.reset_button = ctk.CTkButton(
            self.button_frame,
            text="↺ Reset",
            command=self.reset_typing,
            width=100,
            height=40,
            fg_color="gray",
            font=ctk.CTkFont(size=13)
        )
        self.reset_button.pack(side="left", padx=5)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.button_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#28a745"
        )
        self.status_label.pack(side="right", padx=10)
        
        # Key frequency display
        self.key_freq_frame = ctk.CTkFrame(scrollable)
        self.key_freq_frame.pack(fill="x", padx=10, pady=10)
        
        key_freq_label = ctk.CTkLabel(
            self.key_freq_frame,
            text="Key Frequency (this session)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        key_freq_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        self.key_freq_text = ctk.CTkTextbox(
            self.key_freq_frame,
            height=80,
            font=ctk.CTkFont(size=11),
            state="disabled"
        )
        self.key_freq_text.pack(fill="x", padx=10, pady=(0, 10))
        
    def start_typing(self) -> None:
        """Start a new typing session"""
        self.current_text = random.choice(TYPING_TEXTS)
        self.reference_label.configure(text=self.current_text)
        self.input_textbox.delete("1.0", "end")
        self.start_time = time.time()
        self.is_typing = True
        self.keys_pressed = []
        
        # Update button states
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="Session in progress...", text_color="#ffc107")
        
        self.update_timer()
        logger.info("Typing session started")
        
    def stop_and_save(self) -> None:
        """Stop typing and save session to database"""
        if not self.is_typing:
            return
            
        self.is_typing = False
        
        # Get session data
        session_data = self.get_session_data()
        
        if session_data and session_data['total_chars'] > 0:
            # Calculate key frequency
            from utils.helpers import get_key_frequency
            key_freq = get_key_frequency(self.keys_pressed)
            session_data['key_frequency'] = key_freq
            
            # Save to database
            session_id = self.db.save_session(session_data)
            
            if session_id:
                # Save key frequency
                self.db.save_key_frequency(session_id, key_freq)
                self.status_label.configure(
                    text=f"✓ Session {session_id} saved! WPM: {session_data['wpm']:.1f}",
                    text_color="#28a745"
                )
                logger.info(f"Session {session_id} saved to database")
            else:
                self.status_label.configure(
                    text="✗ Error saving session",
                    text_color="#dc3545"
                )
                logger.error("Failed to save session")
        else:
            self.status_label.configure(
                text="No data to save (type something first!)",
                text_color="#ffc107"
            )
            
        # Update button states
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
    def reset_typing(self) -> None:
        """Reset the typing session"""
        self.start_time = None
        self.is_typing = False
        self.current_text = ""
        self.typed_text = ""
        self.keys_pressed = []
        
        # Reset UI
        self.reference_label.configure(text="Click 'Start New Session' to begin typing practice")
        self.input_textbox.delete("1.0", "end")
        self.wpm_label.configure(text="⚡ WPM: 0")
        self.accuracy_label.configure(text="✓ Accuracy: 100%")
        self.timer_label.configure(text="⏱ Time: 00:00")
        self.chars_label.configure(text="Chars: 0")
        self.status_label.configure(text="")
        
        # Reset button states
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
        # Clear key frequency display
        self.key_freq_text.configure(state="normal")
        self.key_freq_text.delete("1.0", "end")
        self.key_freq_text.configure(state="disabled")
        
    def on_key_release(self, event) -> None:
        """Handle key release events"""
        if not self.is_typing:
            return
            
        # Track keys pressed (only printable characters)
        if event.char and event.char.isprintable():
            self.keys_pressed.append(event.char)
            
        # Get typed text
        self.typed_text = self.input_textbox.get("1.0", "end-1c")
        
        # Calculate statistics
        total_chars = len(self.typed_text)
        correct_chars = sum(1 for a, b in zip(self.typed_text, self.current_text) if a == b)
        
        # Update WPM and accuracy
        if self.start_time:
            elapsed = time.time() - self.start_time
            wpm = calculate_wpm(total_chars, elapsed)
            accuracy = calculate_accuracy(correct_chars, len(self.current_text))
            
            self.wpm_label.configure(text=f"⚡ WPM: {wpm:.1f}")
            self.accuracy_label.configure(text=f"✓ Accuracy: {accuracy:.1f}%")
            self.chars_label.configure(text=f"Chars: {total_chars}")
            
            # Update key frequency display
            self.update_key_frequency_display()
            
    def update_key_frequency_display(self) -> None:
        """Update the key frequency display"""
        if not self.keys_pressed:
            return
            
        from utils.helpers import get_key_frequency
        key_freq = get_key_frequency(self.keys_pressed)
        
        # Sort by frequency
        sorted_keys = sorted(key_freq.items(), key=lambda x: x[1], reverse=True)[:15]
        
        # Format display
        display_text = " | ".join([f"'{k}': {v}" for k, v in sorted_keys])
        
        self.key_freq_text.configure(state="normal")
        self.key_freq_text.delete("1.0", "end")
        self.key_freq_text.insert("1.0", display_text)
        self.key_freq_text.configure(state="disabled")
        
    def update_timer(self) -> None:
        """Update the timer display"""
        if self.is_typing and self.start_time:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.configure(text=f"⏱ Time: {format_duration(elapsed)}")
            self.after(1000, self.update_timer)
            
    def get_session_data(self) -> Optional[Dict]:
        """Get current session data"""
        if not self.start_time:
            return None
            
        elapsed = int(time.time() - self.start_time)
        total_chars = len(self.typed_text)
        correct_chars = sum(1 for a, b in zip(self.typed_text, self.current_text) if a == b)
        
        return {
            'duration': elapsed,
            'total_chars': total_chars,
            'correct_chars': correct_chars,
            'wpm': calculate_wpm(total_chars, elapsed),
            'accuracy': calculate_accuracy(correct_chars, len(self.current_text)),
            'text': self.current_text
        }
