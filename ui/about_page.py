"""
About Page Module
Displays application information and educational security tips
"""

import logging
import customtkinter as ctk
from config import APP_NAME, APP_VERSION, APP_AUTHOR, APP_DESCRIPTION, COLORS
from utils.security_tips import get_all_tips

logger = logging.getLogger(__name__)


class AboutPage(ctk.CTkFrame):
    """About page with application info and security tips"""
    
    def __init__(self, parent) -> None:
        super().__init__(parent, fg_color="transparent")
        self.create_widgets()
        
    def create_widgets(self) -> None:
        """Create all about page widgets"""
        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(self)
        scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header section
        header_frame = ctk.CTkFrame(scrollable)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # App icon and title
        icon_label = ctk.CTkLabel(
            header_frame,
            text="⌨",
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack(pady=(20, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=APP_NAME,
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack()
        
        version_label = ctk.CTkLabel(
            header_frame,
            text=f"Version {APP_VERSION}",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        version_label.pack(pady=(5, 15))
        
        # Description
        desc_frame = ctk.CTkFrame(scrollable)
        desc_frame.pack(fill="x", padx=10, pady=10)
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text="Description",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        desc_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        desc_text = ctk.CTkLabel(
            desc_frame,
            text=APP_DESCRIPTION,
            font=ctk.CTkFont(size=13),
            wraplength=800,
            justify="left"
        )
        desc_text.pack(padx=15, pady=(0, 15), anchor="w")
        
        # Features section
        features_frame = ctk.CTkFrame(scrollable)
        features_frame.pack(fill="x", padx=10, pady=10)
        
        features_label = ctk.CTkLabel(
            features_frame,
            text="Features",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        features_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        features = [
            "Real-time WPM (Words Per Minute) calculation",
            "Typing accuracy tracking",
            "Key frequency analysis",
            "Session history and statistics",
            "PDF report generation",
            "Dark/Light theme support",
            "SQLite database storage",
            "Interactive performance charts"
        ]
        
        for feature in features:
            ctk.CTkLabel(
                features_frame,
                text=f"• {feature}",
                font=ctk.CTkFont(size=12),
                anchor="w"
            ).pack(padx=25, pady=2, anchor="w")
            
        # Add bottom padding
        ctk.CTkFrame(features_frame, height=10, fg_color="transparent").pack()
        
        # Educational Purpose section
        edu_frame = ctk.CTkFrame(scrollable)
        edu_frame.pack(fill="x", padx=10, pady=10)
        
        edu_label = ctk.CTkLabel(
            edu_frame,
            text="Educational Purpose",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        edu_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        edu_text = """This application is designed for educational purposes to help 
cybersecurity students understand:
• Input monitoring concepts (within the application scope)
• Data collection and analysis techniques
• Pattern recognition in user behavior
• Secure coding practices and ethical considerations"""
        
        ctk.CTkLabel(
            edu_frame,
            text=edu_text,
            font=ctk.CTkFont(size=12),
            wraplength=800,
            justify="left"
        ).pack(padx=15, pady=(0, 15), anchor="w")
        
        # Security Disclaimer
        disclaimer_frame = ctk.CTkFrame(scrollable, fg_color=("#fff3cd", "#3d3000"))
        disclaimer_frame.pack(fill="x", padx=10, pady=10)
        
        disclaimer_label = ctk.CTkLabel(
            disclaimer_frame,
            text="⚠ Important Disclaimer",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#856404"
        )
        disclaimer_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        disclaimer_text = """This application ONLY processes keyboard input within its own 
interface. It does NOT:
• Capture system-wide keystrokes
• Run in the background
• Collect data without user consent
• Implement any form of persistence
• Access sensitive system information"""
        
        ctk.CTkLabel(
            disclaimer_frame,
            text=disclaimer_text,
            font=ctk.CTkFont(size=12),
            wraplength=800,
            justify="left",
            text_color="#856404"
        ).pack(padx=15, pady=(0, 15), anchor="w")
        
        # Security Tips section
        tips_frame = ctk.CTkFrame(scrollable)
        tips_frame.pack(fill="x", padx=10, pady=10)
        
        tips_label = ctk.CTkLabel(
            tips_frame,
            text="🛡 Cybersecurity Tips",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        tips_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        tips = get_all_tips()
        
        for tip in tips:
            tip_item = ctk.CTkFrame(tips_frame, fg_color="transparent")
            tip_item.pack(fill="x", padx=15, pady=3)
            
            ctk.CTkLabel(
                tip_item,
                text=f"• {tip['title']}:",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=COLORS['secondary']
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                tip_item,
                text=tip['tip'],
                font=ctk.CTkFont(size=11),
                wraplength=750,
                justify="left"
            ).pack(padx=20, anchor="w")
            
        # Add padding at bottom
        ctk.CTkFrame(tips_frame, height=10, fg_color="transparent").pack()
        
        # Credits section
        credits_frame = ctk.CTkFrame(scrollable)
        credits_frame.pack(fill="x", padx=10, pady=10)
        
        credits_label = ctk.CTkLabel(
            credits_frame,
            text="Credits",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        credits_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        credits_text = f"""Author: {APP_AUTHOR}
Built with: Python, CustomTkinter, SQLite, Matplotlib, ReportLab
License: MIT"""
        
        ctk.CTkLabel(
            credits_frame,
            text=credits_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        ).pack(padx=15, pady=(0, 15), anchor="w")
        
        # Final padding
        ctk.CTkFrame(scrollable, height=30, fg_color="transparent").pack()
