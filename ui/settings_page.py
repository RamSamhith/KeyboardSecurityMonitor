"""
Settings Page Module
Application settings and configuration
"""

import logging
import customtkinter as ctk
from typing import Callable, Optional
from config import COLORS, DATABASE_PATH
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class SettingsPage(ctk.CTkFrame):
    """Settings page for application configuration"""
    
    def __init__(self, parent, db_manager: DatabaseManager, 
                 on_theme_change: Optional[Callable] = None) -> None:
        super().__init__(parent, fg_color="transparent")
        self.db = db_manager
        self.on_theme_change = on_theme_change
        self.create_widgets()
        
    def create_widgets(self) -> None:
        """Create all settings widgets"""
        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(self)
        scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            scrollable,
            text="Settings",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(padx=20, pady=(10, 20), anchor="w")
        
        # Appearance Settings
        self.create_section_header(scrollable, "Appearance")
        
        # Theme switch
        theme_frame = ctk.CTkFrame(scrollable)
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            theme_frame,
            text="Dark Mode",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=15, pady=12)
        
        self.theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="",
            onvalue=True,
            offvalue=False,
            command=self.toggle_theme
        )
        self.theme_switch.pack(side="right", padx=15, pady=12)
        self.theme_switch.select()  # Default to dark mode
        
        # Font size
        font_frame = ctk.CTkFrame(scrollable)
        font_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            font_frame,
            text="Font Size",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=15, pady=12)
        
        self.font_var = ctk.StringVar(value="14")
        font_slider = ctk.CTkSlider(
            font_frame,
            from_=10,
            to=20,
            number_of_steps=10,
            command=self.on_font_change
        )
        font_slider.set(14)
        font_slider.pack(side="right", padx=15, pady=12)
        
        self.font_label = ctk.CTkLabel(
            font_frame,
            text="14",
            font=ctk.CTkFont(size=12),
            width=30
        )
        self.font_label.pack(side="right", padx=5)
        
        # Database Settings
        self.create_section_header(scrollable, "Database")
        
        # Database info
        db_info_frame = ctk.CTkFrame(scrollable)
        db_info_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            db_info_frame,
            text="Database Location:",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        ).pack(padx=15, pady=(10, 0), anchor="w")
        
        ctk.CTkLabel(
            db_info_frame,
            text=str(DATABASE_PATH),
            font=ctk.CTkFont(size=11),
            text_color="gray50"
        ).pack(padx=15, pady=(0, 10), anchor="w")
        
        # Export database
        export_frame = ctk.CTkFrame(scrollable)
        export_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            export_frame,
            text="Export Database",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=15, pady=12)
        
        ctk.CTkButton(
            export_frame,
            text="Export",
            width=80,
            command=self.export_database
        ).pack(side="right", padx=15, pady=12)
        
        # Import database
        import_frame = ctk.CTkFrame(scrollable)
        import_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            import_frame,
            text="Import Database",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=15, pady=12)
        
        ctk.CTkButton(
            import_frame,
            text="Import",
            width=80,
            fg_color="#ffc107",
            text_color="black",
            command=self.import_database
        ).pack(side="right", padx=15, pady=12)
        
        # Danger Zone
        self.create_section_header(scrollable, "Danger Zone", color="#dc3545")
        
        danger_frame = ctk.CTkFrame(scrollable, fg_color=("#ffebee", "#3d1515"))
        danger_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            danger_frame,
            text="Reset All Sessions",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=15, pady=12)
        
        ctk.CTkButton(
            danger_frame,
            text="Reset All",
            width=100,
            fg_color="#dc3545",
            command=self.reset_all_sessions
        ).pack(side="right", padx=15, pady=12)
        
    def create_section_header(self, parent, text: str, 
                               color: str = None) -> None:
        """Create a section header"""
        label = ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=color or COLORS['secondary']
        )
        label.pack(padx=20, pady=(15, 5), anchor="w")
        
    def toggle_theme(self) -> None:
        """Toggle between dark and light theme"""
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
            logger.info("Theme changed to dark")
        else:
            ctk.set_appearance_mode("light")
            logger.info("Theme changed to light")
            
        if self.on_theme_change:
            self.on_theme_change()
            
    def on_font_change(self, value: float) -> None:
        """Handle font size change"""
        size = int(value)
        self.font_label.configure(text=str(size))
        # Font size change would require restarting the app
        # For now, just log it
        logger.info(f"Font size changed to {size}")
        
    def export_database(self) -> None:
        """Export database to a file"""
        from tkinter import filedialog
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")],
            title="Export Database"
        )
        
        if filepath:
            success = self.db.export_database(filepath)
            self.show_message(
                "Export Complete" if success else "Export Failed",
                f"Database exported to:\n{filepath}" if success else "Failed to export database"
            )
            
    def import_database(self) -> None:
        """Import database from a file"""
        from tkinter import filedialog
        
        filepath = filedialog.askopenfilename(
            filetypes=[("Database files", "*.db"), ("All files", "*.*")],
            title="Import Database"
        )
        
        if filepath:
            # Confirm import
            dialog = ctk.CTkToplevel(self)
            dialog.title("Confirm Import")
            dialog.geometry("350x150")
            dialog.transient(self)
            dialog.grab_set()
            
            ctk.CTkLabel(
                dialog,
                text="This will replace your current database.\nContinue?",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            
            def confirm():
                success = self.db.import_database(filepath)
                dialog.destroy()
                self.show_message(
                    "Import Complete" if success else "Import Failed",
                    "Database imported successfully" if success else "Failed to import database"
                )
                
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
                text="Import",
                width=80,
                fg_color="#ffc107",
                text_color="black",
                command=confirm
            ).pack(side="left", padx=10)
            
    def reset_all_sessions(self) -> None:
        """Reset all session history"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Reset")
        dialog.geometry("350x180")
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(
            dialog,
            text="⚠️ WARNING ⚠️\n\nThis will delete ALL session data.\nThis action cannot be undone!",
            font=ctk.CTkFont(size=13),
            text_color="#dc3545"
        ).pack(pady=15)
        
        # Password confirmation
        ctk.CTkLabel(
            dialog,
            text='Type "DELETE" to confirm:',
            font=ctk.CTkFont(size=12)
        ).pack()
        
        confirm_entry = ctk.CTkEntry(dialog, width=150)
        confirm_entry.pack(pady=5)
        
        def confirm():
            if confirm_entry.get() == "DELETE":
                self.db.reset_all_sessions()
                dialog.destroy()
                self.show_message("Reset Complete", "All sessions have been deleted")
            else:
                ctk.CTkLabel(
                    dialog,
                    text="Type DELETE to confirm",
                    text_color="#dc3545"
                ).pack()
                
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
            text="Reset",
            width=80,
            fg_color="#dc3545",
            command=confirm
        ).pack(side="left", padx=10)
        
    def show_message(self, title: str, message: str) -> None:
        """Show a message dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=250
        ).pack(pady=20)
        
        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        ).pack(pady=10)
