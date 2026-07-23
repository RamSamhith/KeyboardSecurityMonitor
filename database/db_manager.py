"""
Database Manager Module
Handles SQLite database operations for typing sessions
"""

import sqlite3
import shutil
import logging
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from config import DATABASE_PATH

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database operations for typing sessions"""
    
    def __init__(self) -> None:
        """Initialize database connection and create tables"""
        self.db_path: Path = DATABASE_PATH
        self.connection: Optional[sqlite3.Connection] = None
        self.create_tables()
        
    def connect(self) -> bool:
        """Create database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            logger.info(f"Connected to database: {self.db_path}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            return False
            
    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")
            
    def create_tables(self) -> None:
        """Create database tables if they don't exist"""
        if not self.connect():
            return
            
        try:
            cursor = self.connection.cursor()
            
            # Typing sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS typing_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    duration_seconds INTEGER,
                    total_characters INTEGER,
                    correct_characters INTEGER,
                    wpm REAL,
                    accuracy REAL,
                    text_practiced TEXT
                )
            """)
            
            # Key frequency table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS key_frequency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    key_char TEXT,
                    frequency INTEGER,
                    FOREIGN KEY (session_id) REFERENCES typing_sessions(id)
                )
            """)
            
            self.connection.commit()
            logger.info("Database tables created successfully")
            
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
        finally:
            self.disconnect()
            
    def save_session(self, session_data: Dict) -> Optional[int]:
        """Save typing session data and return session ID"""
        if not self.connect():
            return None
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO typing_sessions 
                (duration_seconds, total_characters, correct_characters, wpm, accuracy, text_practiced)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session_data['duration'],
                session_data['total_chars'],
                session_data['correct_chars'],
                session_data['wpm'],
                session_data['accuracy'],
                session_data['text']
            ))
            
            session_id = cursor.lastrowid
            self.connection.commit()
            logger.info(f"Session saved with ID: {session_id}")
            return session_id
            
        except sqlite3.Error as e:
            logger.error(f"Error saving session: {e}")
            return None
        finally:
            self.disconnect()
            
    def save_key_frequency(self, session_id: int, key_freq: Dict[str, int]) -> bool:
        """Save key frequency data for a session"""
        if not self.connect():
            return False
            
        try:
            cursor = self.connection.cursor()
            for key, freq in key_freq.items():
                cursor.execute("""
                    INSERT INTO key_frequency (session_id, key_char, frequency)
                    VALUES (?, ?, ?)
                """, (session_id, key, freq))
            
            self.connection.commit()
            logger.info(f"Key frequency saved for session {session_id}")
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Error saving key frequency: {e}")
            return False
        finally:
            self.disconnect()
            
    def get_all_sessions(self) -> List[Dict]:
        """Retrieve all typing sessions sorted by date (newest first)"""
        if not self.connect():
            return []
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM typing_sessions ORDER BY session_date DESC")
            sessions = cursor.fetchall()
            return [dict(session) for session in sessions]
            
        except sqlite3.Error as e:
            logger.error(f"Error fetching sessions: {e}")
            return []
        finally:
            self.disconnect()
            
    def get_session_by_id(self, session_id: int) -> Optional[Dict]:
        """Retrieve a specific session by ID"""
        if not self.connect():
            return None
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM typing_sessions WHERE id = ?", (session_id,))
            session = cursor.fetchone()
            return dict(session) if session else None
            
        except sqlite3.Error as e:
            logger.error(f"Error fetching session {session_id}: {e}")
            return None
        finally:
            self.disconnect()
            
    def get_session_count(self) -> int:
        """Get total number of sessions"""
        if not self.connect():
            return 0
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM typing_sessions")
            count = cursor.fetchone()[0]
            return count
            
        except sqlite3.Error as e:
            logger.error(f"Error counting sessions: {e}")
            return 0
        finally:
            self.disconnect()
            
    def get_statistics(self) -> Dict:
        """Get aggregated statistics from all sessions"""
        if not self.connect():
            return {
                'total_sessions': 0,
                'avg_wpm': 0.0,
                'best_wpm': 0.0,
                'avg_accuracy': 0.0,
                'today_sessions': 0,
                'total_characters': 0
            }
            
        try:
            cursor = self.connection.cursor()
            
            # Get overall statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_sessions,
                    COALESCE(AVG(wpm), 0) as avg_wpm,
                    COALESCE(MAX(wpm), 0) as best_wpm,
                    COALESCE(AVG(accuracy), 0) as avg_accuracy,
                    COALESCE(SUM(total_characters), 0) as total_characters
                FROM typing_sessions
            """)
            stats = dict(cursor.fetchone())
            
            # Get today's sessions count
            today = date.today().isoformat()
            cursor.execute("""
                SELECT COUNT(*) FROM typing_sessions 
                WHERE DATE(session_date) = ?
            """, (today,))
            stats['today_sessions'] = cursor.fetchone()[0]
            
            return stats
            
        except sqlite3.Error as e:
            logger.error(f"Error fetching statistics: {e}")
            return {
                'total_sessions': 0,
                'avg_wpm': 0.0,
                'best_wpm': 0.0,
                'avg_accuracy': 0.0,
                'today_sessions': 0,
                'total_characters': 0
            }
        finally:
            self.disconnect()
            
    def get_recent_sessions(self, limit: int = 5) -> List[Dict]:
        """Get recent typing sessions"""
        if not self.connect():
            return []
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM typing_sessions 
                ORDER BY session_date DESC 
                LIMIT ?
            """, (limit,))
            sessions = cursor.fetchall()
            return [dict(session) for session in sessions]
            
        except sqlite3.Error as e:
            logger.error(f"Error fetching recent sessions: {e}")
            return []
        finally:
            self.disconnect()
            
    def search_sessions(self, query: str) -> List[Dict]:
        """Search sessions by text practiced"""
        if not self.connect():
            return []
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM typing_sessions 
                WHERE text_practiced LIKE ?
                ORDER BY session_date DESC
            """, (f"%{query}%",))
            sessions = cursor.fetchall()
            return [dict(session) for session in sessions]
            
        except sqlite3.Error as e:
            logger.error(f"Error searching sessions: {e}")
            return []
        finally:
            self.disconnect()
            
    def delete_session(self, session_id: int) -> bool:
        """Delete a specific session and its key frequency data"""
        if not self.connect():
            return False
            
        try:
            cursor = self.connection.cursor()
            
            # Delete key frequency records first
            cursor.execute("DELETE FROM key_frequency WHERE session_id = ?", (session_id,))
            
            # Delete the session
            cursor.execute("DELETE FROM typing_sessions WHERE id = ?", (session_id,))
            
            self.connection.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                logger.info(f"Session {session_id} deleted")
            return deleted
            
        except sqlite3.Error as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            return False
        finally:
            self.disconnect()
            
    def reset_all_sessions(self) -> bool:
        """Delete all sessions and key frequency data"""
        if not self.connect():
            return False
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM key_frequency")
            cursor.execute("DELETE FROM typing_sessions")
            self.connection.commit()
            logger.info("All sessions reset")
            return True
            
        except sqlite3.Error as e:
            logger.error(f"Error resetting sessions: {e}")
            return False
        finally:
            self.disconnect()
            
    def export_database(self, destination: str) -> bool:
        """Export database to a new location"""
        try:
            self.disconnect()  # Ensure connection is closed before copy
            shutil.copy2(self.db_path, destination)
            logger.info(f"Database exported to {destination}")
            return True
        except Exception as e:
            logger.error(f"Error exporting database: {e}")
            return False
            
    def import_database(self, source: str) -> bool:
        """Import database from a file"""
        try:
            self.disconnect()  # Ensure connection is closed before copy
            shutil.copy2(source, self.db_path)
            logger.info(f"Database imported from {source}")
            return True
        except Exception as e:
            logger.error(f"Error importing database: {e}")
            return False
