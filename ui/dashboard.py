"""
Dashboard Page Module
Displays statistics overview and recent activity
"""

import logging
import customtkinter as ctk
from config import COLORS
from database.db_manager import DatabaseManager
from utils.security_tips import get_random_tip

logger = logging.getLogger(__name__)


class DashboardPage(ctk.CTkFrame):
    """Dashboard page showing statistics and recent activity"""
    
    def __init__(self, parent, db_manager: DatabaseManager, navigate_callback=None) -> None:
        super().__init__(parent, fg_color="transparent")
        self.db = db_manager
        self.navigate_callback = navigate_callback
        self.create_widgets()
        self.refresh_data()
        
    def create_widgets(self) -> None:
        """Create all dashboard widgets"""
        # Scrollable frame
        self.scrollable = ctk.CTkScrollableFrame(self)
        self.scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            self.scrollable,
            text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(padx=20, pady=(10, 20), anchor="w")
        
        # Stats cards frame
        self.stats_frame = ctk.CTkFrame(self.scrollable, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=10, pady=5)
        
        # Create stat cards
        self.create_stat_cards()
        
        # Quick actions frame
        self.actions_frame = ctk.CTkFrame(self.scrollable)
        self.actions_frame.pack(fill="x", padx=10, pady=10)
        
        actions_label = ctk.CTkLabel(
            self.actions_frame,
            text="Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        actions_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        # Quick action buttons
        btn_frame = ctk.CTkFrame(self.actions_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(
            btn_frame,
            text="Start Typing Practice",
            width=180,
            height=40,
            command=lambda: self.navigate_callback("typing_practice") if self.navigate_callback else None
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Generate Report",
            width=180,
            height=40,
            fg_color="#28a745",
            command=lambda: self.navigate_callback("reports") if self.navigate_callback else None
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="View Statistics",
            width=180,
            height=40,
            fg_color="#6c757d",
            command=lambda: self.navigate_callback("statistics") if self.navigate_callback else None
        ).pack(side="left", padx=5)
        
        # Charts frame
        self.charts_frame = ctk.CTkFrame(self.scrollable)
        self.charts_frame.pack(fill="x", padx=10, pady=10)
        
        charts_label = ctk.CTkLabel(
            self.charts_frame,
            text="Performance Charts",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        charts_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        # Chart placeholder
        self.chart_container = ctk.CTkFrame(self.charts_frame, fg_color="transparent")
        self.chart_container.pack(fill="x", padx=15, pady=(0, 15))
        
        self.chart_label = ctk.CTkLabel(
            self.chart_container,
            text="Complete some typing sessions to see charts",
            font=ctk.CTkFont(size=13),
            text_color="gray60"
        )
        self.chart_label.pack(pady=30)
        
        # Recent activity frame
        self.recent_frame = ctk.CTkFrame(self.scrollable)
        self.recent_frame.pack(fill="x", padx=10, pady=10)
        
        recent_label = ctk.CTkLabel(
            self.recent_frame,
            text="Recent Activity",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        recent_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        self.activity_container = ctk.CTkFrame(self.recent_frame, fg_color="transparent")
        self.activity_container.pack(fill="x", padx=15, pady=(0, 15))
        
        # Security tip
        self.tip_frame = ctk.CTkFrame(self.scrollable)
        self.tip_frame.pack(fill="x", padx=10, pady=10)
        
        tip_label = ctk.CTkLabel(
            self.tip_frame,
            text="Security Tip",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        tip_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        tip = get_random_tip()
        
        tip_title = ctk.CTkLabel(
            self.tip_frame,
            text=tip['title'],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS['secondary']
        )
        tip_title.pack(padx=15, anchor="w")
        
        tip_text = ctk.CTkLabel(
            self.tip_frame,
            text=tip['tip'],
            font=ctk.CTkFont(size=13),
            wraplength=700,
            justify="left"
        )
        tip_text.pack(padx=15, pady=(0, 15), anchor="w")
        
    def create_stat_cards(self) -> None:
        """Create statistics cards"""
        card_data = [
            ("Total Sessions", "0", "sessions_icon"),
            ("Average WPM", "0", "wpm_icon"),
            ("Best WPM", "0", "best_icon"),
            ("Accuracy", "0%", "accuracy_icon"),
            ("Today's Sessions", "0", "today_icon"),
            ("Total Characters", "0", "chars_icon")
        ]
        
        self.stat_values = {}
        
        # Create 3 columns x 2 rows of cards
        for idx, (title, default_val, key) in enumerate(card_data):
            row = idx // 3
            col = idx % 3
            
            card = ctk.CTkFrame(self.stats_frame, height=90)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            self.stats_frame.grid_columnconfigure(col, weight=1)
            
            # Icon placeholder (using unicode)
            icon_map = {
                "sessions_icon": "📊",
                "wpm_icon": "⚡",
                "best_icon": "🏆",
                "accuracy_icon": "✓",
                "today_icon": "📅",
                "chars_icon": "⌨"
            }
            
            ctk.CTkLabel(
                card,
                text=f"{icon_map.get(key, '•')}",
                font=ctk.CTkFont(size=20)
            ).pack(pady=(8, 0))
            
            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=11),
                text_color="gray60"
            ).pack()
            
            value_label = ctk.CTkLabel(
                card,
                text=default_val,
                font=ctk.CTkFont(size=22, weight="bold")
            )
            value_label.pack(pady=(0, 8))
            
            self.stat_values[key] = value_label
            
    def refresh_data(self) -> None:
        """Refresh all dashboard data from database"""
        try:
            stats = self.db.get_statistics()
            
            # Update stat cards
            self.stat_values['sessions_icon'].configure(
                text=str(stats.get('total_sessions', 0))
            )
            self.stat_values['wpm_icon'].configure(
                text=f"{stats.get('avg_wpm', 0):.1f}"
            )
            self.stat_values['best_icon'].configure(
                text=f"{stats.get('best_wpm', 0):.1f}"
            )
            self.stat_values['accuracy_icon'].configure(
                text=f"{stats.get('avg_accuracy', 0):.1f}%"
            )
            self.stat_values['today_icon'].configure(
                text=str(stats.get('today_sessions', 0))
            )
            self.stat_values['chars_icon'].configure(
                text=f"{stats.get('total_characters', 0):,}"
            )
            
            # Update recent activity
            self.update_recent_activity()
            
        except Exception as e:
            logger.error(f"Error refreshing dashboard: {e}")
            
    def update_recent_activity(self) -> None:
        """Update recent activity section"""
        # Clear existing items
        for widget in self.activity_container.winfo_children():
            widget.destroy()
            
        recent = self.db.get_recent_sessions(limit=5)
        
        if not recent:
            ctk.CTkLabel(
                self.activity_container,
                text="No recent activity. Start a typing session!",
                font=ctk.CTkFont(size=13),
                text_color="gray60"
            ).pack(pady=20)
            return
            
        for session in recent:
            row_frame = ctk.CTkFrame(self.activity_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            # Session info
            date_str = session.get('session_date', 'Unknown')
            if 'T' in str(date_str):
                date_str = str(date_str).split('T')[0]
                
            ctk.CTkLabel(
                row_frame,
                text=f"Session on {date_str}",
                font=ctk.CTkFont(size=12),
                anchor="w"
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row_frame,
                text=f"WPM: {session.get('wpm', 0):.1f} | Accuracy: {session.get('accuracy', 0):.1f}%",
                font=ctk.CTkFont(size=12),
                text_color="gray50"
            ).pack(side="right", padx=5)
