"""
Reports Page Module
Handles PDF report generation and display
"""

import logging
import customtkinter as ctk
from config import REPORTS_DIR
from database.db_manager import DatabaseManager
from reports.pdf_generator import PDFGenerator

logger = logging.getLogger(__name__)


class ReportsPage(ctk.CTkFrame):
    """Reports page for generating and viewing PDF reports"""
    
    def __init__(self, parent, db_manager: DatabaseManager) -> None:
        super().__init__(parent, fg_color="transparent")
        self.db = db_manager
        self.pdf_gen = PDFGenerator()
        self.create_widgets()
        
    def create_widgets(self) -> None:
        """Create all reports page widgets"""
        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(self)
        scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            scrollable,
            text="📄 Reports",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(padx=20, pady=(10, 20), anchor="w")
        
        # Report generation section
        gen_frame = ctk.CTkFrame(scrollable)
        gen_frame.pack(fill="x", padx=10, pady=10)
        
        gen_label = ctk.CTkLabel(
            gen_frame,
            text="Generate Reports",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        gen_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        # Single session report
        single_frame = ctk.CTkFrame(gen_frame, fg_color="transparent")
        single_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(
            single_frame,
            text="Generate report for the most recent session:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            single_frame,
            text="Generate Single Report",
            width=180,
            command=self.generate_single_report
        ).pack(side="right", padx=5)
        
        # Summary report
        summary_frame = ctk.CTkFrame(gen_frame, fg_color="transparent")
        summary_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(
            summary_frame,
            text="Generate summary of all sessions:",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            summary_frame,
            text="Generate Summary Report",
            width=180,
            fg_color="#28a745",
            command=self.generate_summary_report
        ).pack(side="right", padx=5)
        
        # Session count info
        session_count = self.db.get_session_count()
        info_frame = ctk.CTkFrame(gen_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=(10, 15))
        
        ctk.CTkLabel(
            info_frame,
            text=f"ℹ Total sessions in database: {session_count}",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        ).pack(side="left")
        
        # Recent reports section
        recent_frame = ctk.CTkFrame(scrollable)
        recent_frame.pack(fill="x", padx=10, pady=10)
        
        recent_label = ctk.CTkLabel(
            recent_frame,
            text="Recent Reports",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        recent_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        # Reports list
        self.reports_list_frame = ctk.CTkFrame(recent_frame, fg_color="transparent")
        self.reports_list_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.refresh_reports_list()
        
        # Refresh button
        ctk.CTkButton(
            recent_frame,
            text="Refresh List",
            width=100,
            fg_color="gray",
            command=self.refresh_reports_list
        ).pack(padx=15, pady=(0, 15), anchor="w")
        
        # Educational section
        edu_frame = ctk.CTkFrame(scrollable)
        edu_frame.pack(fill="x", padx=10, pady=10)
        
        edu_label = ctk.CTkLabel(
            edu_frame,
            text="Understanding Your Reports",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        edu_label.pack(padx=15, pady=(10, 5), anchor="w")
        
        explanations = [
            ("WPM (Words Per Minute)", "Measures typing speed. Average is 40-60 WPM."),
            ("Accuracy", "Percentage of correctly typed characters. Aim for 95%+."),
            ("Key Frequency", "Shows which keys you use most. Helps identify patterns."),
            ("Duration", "Total time spent typing in the session.")
        ]
        
        for title, desc in explanations:
            item_frame = ctk.CTkFrame(edu_frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=15, pady=3)
            
            ctk.CTkLabel(
                item_frame,
                text=f"• {title}:",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(side="left")
            
            ctk.CTkLabel(
                item_frame,
                text=desc,
                font=ctk.CTkFont(size=11),
                text_color="gray60"
            ).pack(side="left", padx=5)
            
        # Add padding at bottom
        ctk.CTkFrame(scrollable, height=20, fg_color="transparent").pack()
        
    def generate_single_report(self) -> None:
        """Generate PDF report for the most recent session"""
        sessions = self.db.get_all_sessions()
        
        if not sessions:
            self.show_message("No Sessions", "No typing sessions found.\nComplete a practice session first!")
            return
            
        # Get most recent session
        recent_session = sessions[0]
        
        # Add key frequency if available
        filepath = self.pdf_gen.generate_session_report(recent_session)
        
        if filepath:
            self.show_message(
                "Report Generated",
                f"Report saved to:\n{filepath.name}\n\nLocation: {REPORTS_DIR}"
            )
            self.refresh_reports_list()
        else:
            self.show_message("Error", "Failed to generate report")
            
    def generate_summary_report(self) -> None:
        """Generate summary report for all sessions"""
        sessions = self.db.get_all_sessions()
        
        if not sessions:
            self.show_message("No Sessions", "No typing sessions found.\nComplete a practice session first!")
            return
            
        filepath = self.pdf_gen.generate_summary_report(sessions)
        
        if filepath:
            self.show_message(
                "Summary Generated",
                f"Summary saved to:\n{filepath.name}\n\nLocation: {REPORTS_DIR}\n\nTotal sessions included: {len(sessions)}"
            )
            self.refresh_reports_list()
        else:
            self.show_message("Error", "Failed to generate summary report")
            
    def refresh_reports_list(self) -> None:
        """Refresh the list of generated reports"""
        # Clear existing items
        for widget in self.reports_list_frame.winfo_children():
            widget.destroy()
            
        # Get list of PDF files
        try:
            pdf_files = sorted(REPORTS_DIR.glob("*.pdf"), reverse=True)
        except Exception as e:
            logger.error(f"Error listing reports: {e}")
            pdf_files = []
            
        if not pdf_files:
            ctk.CTkLabel(
                self.reports_list_frame,
                text="No reports generated yet.",
                font=ctk.CTkFont(size=13),
                text_color="gray60"
            ).pack(pady=20)
            return
            
        # Show latest 10 reports
        for pdf_file in list(pdf_files)[:10]:
            item_frame = ctk.CTkFrame(self.reports_list_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=2)
            
            # File icon and name
            ctk.CTkLabel(
                item_frame,
                text="📄",
                font=ctk.CTkFont(size=14)
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                item_frame,
                text=pdf_file.name,
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=5)
            
            # File size
            size_kb = pdf_file.stat().st_size / 1024
            ctk.CTkLabel(
                item_frame,
                text=f"{size_kb:.1f} KB",
                font=ctk.CTkFont(size=11),
                text_color="gray50"
            ).pack(side="right", padx=5)
            
    def show_message(self, title: str, message: str) -> None:
        """Show a message dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("350x180")
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=13),
            wraplength=300,
            justify="left"
        ).pack(pady=20, padx=20)
        
        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            command=dialog.destroy
        ).pack(pady=10)
