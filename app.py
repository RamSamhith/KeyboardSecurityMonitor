"""
Keyboard Security Monitor
Main Application Entry Point

An educational cybersecurity desktop application for monitoring
and analyzing keyboard typing patterns.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import APP_NAME, APP_VERSION, LOG_FORMAT, LOG_LEVEL, LOG_FILE
from ui.main_window import MainWindow

def setup_logging():
    """Configure application logging"""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def main():
    """Main application entry point"""
    logger = setup_logging()
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    
    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
