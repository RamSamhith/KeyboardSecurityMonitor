"""
Statistics Page Module
Displays session history with search, delete, and export
"""

import logging
import customtkinter as ctk
from typing import List, Dict
from database.db_manager import DatabaseManager
from reports.pdf_generator import PDFGenerator

logger = logging.getLogger(__name__)


class StatisticsPage(ctk.CTkFrame):
    """Statistics page showing session history"""
    
    def __init__(self, parent, db_manager: DatabaseManager) -> None:
        super().__init__(parent, fg_color="transparent")
        self.db = db_manager
        self.pdf_gen = PDFGenerator()
        self.create_widgets()
        self.refresh_sessions()
        
    def create_widgets(self) -> None:
        """Create all statistics page widgets"""
        # Title row with search
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 5))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Statistics",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(side="left")
        
        # Search frame
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.pack(side="right")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search sessions...",
            width=250
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_sessions())
        
        ctk.CTkButton(
            search_frame,
            text="Search",
            width=80,
            command=self.search_sessions
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            search_frame,
            text="Clear",
            width=60,
            fg_color="gray",
            command=self.clear_search
        ).pack(side="left")
        
        # Action buttons
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkButton(
            action_frame,
            text="Export Selected as PDF",
            width=160,
            command=self.export_selected_pdf
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            action_frame,
            text="Delete Selected",
            width=140,
            fg_color="#dc3545",
            command=self.delete_selected
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            action_frame,
            text="Refresh",
            width=80,
            fg_color="gray",
            command=self.refresh_sessions
        ).pack(side="right", padx=5)
        
        # Sessions table
        self.create_sessions_table()
        
    def create_sessions_table(self) -> None:
        """Create scrollable sessions table"""
        # Table container
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Header row
        header = ctk.CTkFrame(table_frame, fg_color=("gray85", "gray25"))
        header.pack(fill="x")
        
        headers = ["Select", "Date", "Duration", "WPM", "Accuracy", "Characters", "ID"]
        widths = [50, 120, 100, 70, 80, 100, 50]
        
        for header_text, width in zip(headers, widths):
            ctk.CTkLabel(
                header,
                text=header_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=width
            ).pack(side="left", padx=5, pady=8)
            
        # Scrollable rows
        self.sessions_scroll = ctk.CTkScrollableFrame(table_frame)
        self.sessions_scroll.pack(fill="both", expand=True)
        
        self.session_rows = []
        self.session_checkboxes = []
        
    def refresh_sessions(self) -> None:
        """Refresh sessions list from database"""
        # Clear existing rows
        for widget in self.sessions_scroll.winfo_children():
            widget.destroy()
        self.session_rows.clear()
        self.session_checkboxes.clear()
        
        sessions = self.db.get_all_sessions()
        
        if not sessions:
            ctk.CTkLabel(
                self.sessions_scroll,
                text="No sessions found. Start a typing practice!",
                font=ctk.CTkFont(size=14),
                text_color="gray60"
            ).pack(pady=40)
            return
            
        for session in sessions:
            self.add_session_row(session)
            
    def add_session_row(self, session: Dict) -> None:
        """Add a single session row to the table"""
        row_frame = ctk.CTkFrame(self.sessions_scroll, fg_color="transparent")
        row_frame.pack(fill="x", pady=2)
        
        # Checkbox
        var = ctk.BooleanVar(value=False)
        checkbox = ctk.CTkCheckBox(
            row_frame,
            text="",
            variable=var,
            width=40
        )
        checkbox.pack(side="left", padx=5)
        self.session_checkboxes.append((var, session.get('id')))
        
        # Date
        date_str = str(session.get('session_date', ''))[:19]
        ctk.CTkLabel(
            row_frame,
            text=date_str,
            font=ctk.CTkFont(size=11),
            width=120
        ).pack(side="left", padx=5)
        
        # Duration
        duration = session.get('duration_seconds', 0)
        ctk.CTkLabel(
            row_frame,
            text=f"{duration}s",
            font=ctk.CTkFont(size=11),
            width=100
        ).pack(side="left", padx=5)
        
        # WPM
        ctk.CTkLabel(
            row_frame,
            text=f"{session.get('wpm', 0):.1f}",
            font=ctk.CTkFont(size=11),
            width=70
        ).pack(side="left", padx=5)
        
        # Accuracy
        ctk.CTkLabel(
            row_frame,
            text=f"{session.get('accuracy', 0):.1f}%",
            font=ctk.CTkFont(size=11),
            width=80
        ).pack(side="left", padx=5)
        
        # Total characters
        ctk.CTkLabel(
            row_frame,
            text=str(session.get('total_characters', 0)),
            font=ctk.CTkFont(size=11),
            width=100
        ).pack(side="left", padx=5)
        
        # ID
        ctk.CTkLabel(
            row_frame,
            text=str(session.get('id', '')),
            font=ctk.CTkFont(size=11),
            width=50
        ).pack(side="left", padx=5)
        
        self.session_rows.append(row_frame)
        
    def search_sessions(self) -> None:
        """Search sessions by query"""
        query = self.search_entry.get().strip()
        
        # Clear existing rows
        for widget in self.sessions_scroll.winfo_children():
            widget.destroy()
        self.session_rows.clear()
        self.session_checkboxes.clear()
        
        if not query:
            self.refresh_sessions()
            return
            
        sessions = self.db.search_sessions(query)
        
        if not sessions:
            ctk.CTkLabel(
                self.sessions_scroll,
                text=f"No sessions found for '{query}'",
                font=ctk.CTkFont(size=14),
                text_color="gray60"
            ).pack(pady=40)
            return
            
        for session in sessions:
            self.add_session_row(session)
            
    def clear_search(self) -> None:
        """Clear search and show all sessions"""
        self.search_entry.delete(0, "end")
        self.refresh_sessions()
        
    def get_selected_sessions(self) -> List[Dict]:
        """Get list of selected sessions"""
        selected = []
        for var, session_id in self.session_checkboxes:
            if var.get():
                session = self.db.get_session_by_id(session_id)
                if session:
                    selected.append(session)
        return selected
        
    def delete_selected(self) -> None:
        """Delete selected sessions"""
        selected = self.get_selected_sessions()
        if not selected:
            return
            
        # Confirm dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Delete")
        dialog.geometry("300x150")
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(
            dialog,
            text=f"Delete {len(selected)} session(s)?",
            font=ctk.CTkFont(size=14)
        ).pack(pady=20)
        
        def confirm():
            for session in selected:
                self.db.delete_session(session['id'])
            dialog.destroy()
            self.refresh_sessions()
            
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=80,
            fg_color="gray",
            command=dialog.destroy
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Delete",
            width=80,
            fg_color="#dc3545",
            command=confirm
        ).pack(side="left", padx=10)
        
    def export_selected_pdf(self) -> None:
        """Export selected sessions as PDF"""
        selected = self.get_selected_sessions()
        if not selected:
            # Show message if nothing selected
            dialog = ctk.CTkToplevel(self)
            dialog.title("No Selection")
            dialog.geometry("250x100")
            dialog.transient(self)
            dialog.grab_set()
            
            ctk.CTkLabel(
                dialog,
                text="Please select sessions to export",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            
            ctk.CTkButton(
                dialog,
                text="OK",
                command=dialog.destroy
            ).pack(pady=10)
            return
            
        # Generate PDF for each selected session
        for session in selected:
            filepath = self.pdf_gen.generate_session_report(session)
            if filepath:
                logger.info(f"Exported session {session['id']} to {filepath}")
                
        # Show success message
        dialog = ctk.CTkToplevel(self)
        dialog.title("Export Complete")
        dialog.geometry("300x120")
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(
            dialog,
            text=f"Exported {len(selected)} report(s) to reports folder",
            font=ctk.CTkFont(size=14)
        ).pack(pady=20)
        
        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        ).pack(pady=10)
