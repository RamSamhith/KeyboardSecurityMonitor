"""
Main Window Module
Creates the main application window and navigation
"""

import logging
import customtkinter as ctk
from typing import Optional
from config import APP_NAME, APP_VERSION
from database.db_manager import DatabaseManager
from ui.dashboard import DashboardPage
from ui.typing_page import TypingPage
from ui.statistics_page import StatisticsPage
from ui.settings_page import SettingsPage
from ui.reports_page import ReportsPage
from ui.about_page import AboutPage

logger = logging.getLogger(__name__)


class MainWindow(ctk.CTk):
    """Main application window with navigation"""
    
    def __init__(self) -> None:
        super().__init__()
        
        # Initialize database manager
        self.db = DatabaseManager()
        
        # Current page reference
        self.current_page: Optional[ctk.CTkFrame] = None
        
        # Window configuration
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1200x800")
        self.minsize(1000, 600)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create UI elements
        self.create_sidebar()
        self.create_main_content()
        
        # Show default page
        self.show_page("dashboard")
        
    def create_sidebar(self) -> None:
        """Create navigation sidebar"""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)
        
        # Logo/Title
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="ew")
        
        ctk.CTkLabel(
            self.logo_frame, 
            text="⌨",
            font=ctk.CTkFont(size=32)
        ).pack()
        
        ctk.CTkLabel(
            self.logo_frame, 
            text="Keyboard\nSecurity Monitor",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(5, 0))
        
        # Separator
        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray50").grid(
            row=1, column=0, padx=20, pady=10, sticky="ew"
        )
        
        # Navigation buttons with icons
        nav_items = [
            ("📊 Dashboard", "dashboard"),
            ("⌨ Typing Practice", "typing_practice"),
            ("📈 Statistics", "statistics"),
            ("📄 Reports", "reports"),
            ("⚙ Settings", "settings"),
            ("ℹ About", "about")
        ]
        
        self.nav_buttons = {}
        for idx, (text, page) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                height=40,
                corner_radius=5,
                font=ctk.CTkFont(size=13),
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                command=lambda p=page: self.show_page(p)
            )
            btn.grid(row=idx + 2, column=0, padx=15, pady=3, sticky="ew")
            self.nav_buttons[page] = btn
            
        # Version info at bottom
        ctk.CTkLabel(
            self.sidebar,
            text=f"v{APP_VERSION}",
            font=ctk.CTkFont(size=10),
            text_color="gray50"
        ).grid(row=9, column=0, padx=20, pady=10)
        
    def create_main_content(self) -> None:
        """Create main content area"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
    def show_page(self, page_name: str) -> None:
        """Show selected page"""
        # Clear current content
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Update navigation button states
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")
                
        # Create page content based on selection
        try:
            if page_name == "dashboard":
                self.current_page = DashboardPage(self.main_frame, self.db, self.show_page)
            elif page_name == "typing_practice":
                self.current_page = TypingPage(self.main_frame, self.db)
            elif page_name == "statistics":
                self.current_page = StatisticsPage(self.main_frame, self.db)
            elif page_name == "reports":
                self.current_page = ReportsPage(self.main_frame, self.db)
            elif page_name == "settings":
                self.current_page = SettingsPage(
                    self.main_frame, 
                    self.db,
                    on_theme_change=self.on_theme_change
                )
            elif page_name == "about":
                self.current_page = AboutPage(self.main_frame)
            else:
                self.current_page = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                ctk.CTkLabel(
                    self.current_page,
                    text="Page not found",
                    font=ctk.CTkFont(size=16)
                ).pack(expand=True)
                
            if self.current_page:
                self.current_page.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
                
        except Exception as e:
            logger.error(f"Error loading page {page_name}: {e}")
            error_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            error_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            
            ctk.CTkLabel(
                error_frame,
                text="Error loading page",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#dc3545"
            ).pack(pady=20)
            
            ctk.CTkLabel(
                error_frame,
                text=str(e),
                font=ctk.CTkFont(size=12),
                text_color="gray60"
            ).pack()
            
    def on_theme_change(self) -> None:
        """Handle theme change"""
        logger.info("Theme changed")
        # Refresh current page if needed
        if self.current_page:
            current_page_name = None
            for name, btn in self.nav_buttons.items():
                if btn.cget("fg_color") == ("gray75", "gray25"):
                    current_page_name = name
                    break
            # Optionally refresh the page
