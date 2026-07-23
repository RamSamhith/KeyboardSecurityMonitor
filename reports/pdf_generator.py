"""
PDF Report Generator Module
Generates professional PDF reports for typing sessions
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from config import REPORTS_DIR

logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generates professional PDF reports for typing sessions"""
    
    def __init__(self) -> None:
        self.output_dir: Path = REPORTS_DIR
        
    def generate_session_report(self, session_data: Dict, 
                                 output_filename: Optional[str] = None) -> Optional[Path]:
        """Generate a comprehensive PDF report for a typing session"""
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"typing_report_{timestamp}.pdf"
            
        filepath = self.output_dir / output_filename
        
        try:
            c = canvas.Canvas(str(filepath), pagesize=letter)
            width, height = letter
            
            # Header background
            c.setFillColor(colors.HexColor("#1f538d"))
            c.rect(0, height - 100, width, 100, fill=True, stroke=False)
            
            # Title
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 24)
            c.drawString(72, height - 60, "Typing Session Report")
            
            # Subtitle
            c.setFont("Helvetica", 12)
            c.drawString(72, height - 85, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Session Date
            y_position = height - 140
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(72, y_position, "Session Information")
            
            # Draw a line
            y_position -= 5
            c.setStrokeColor(colors.HexColor("#1f538d"))
            c.setLineWidth(2)
            c.line(72, y_position, width - 72, y_position)
            
            y_position -= 25
            c.setFont("Helvetica", 11)
            
            session_date = session_data.get('session_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if 'T' in str(session_date):
                session_date = str(session_date).replace('T', ' ')[:19]
                
            info_lines = [
                f"Session ID: {session_data.get('id', 'N/A')}",
                f"Date: {session_date}",
                f"Text Practiced: {session_data.get('text_practiced', session_data.get('text', 'N/A'))[:80]}..."
            ]
            
            for line in info_lines:
                c.drawString(90, y_position, line)
                y_position -= 20
                
            # Performance Statistics
            y_position -= 20
            c.setFont("Helvetica-Bold", 14)
            c.drawString(72, y_position, "Performance Statistics")
            
            y_position -= 5
            c.line(72, y_position, width - 72, y_position)
            
            y_position -= 25
            c.setFont("Helvetica", 11)
            
            duration = session_data.get('duration_seconds', session_data.get('duration', 0))
            wpm = session_data.get('wpm', 0)
            accuracy = session_data.get('accuracy', 0)
            total_chars = session_data.get('total_characters', session_data.get('total_chars', 0))
            correct_chars = session_data.get('correct_characters', session_data.get('correct_chars', 0))
            
            # Calculate grade
            if wpm >= 60 and accuracy >= 95:
                grade = "Excellent"
            elif wpm >= 40 and accuracy >= 85:
                grade = "Good"
            elif wpm >= 20 and accuracy >= 70:
                grade = "Average"
            else:
                grade = "Needs Improvement"
            
            stats = [
                f"Duration: {duration} seconds",
                f"Words Per Minute (WPM): {wpm:.1f}",
                f"Accuracy: {accuracy:.1f}%",
                f"Total Characters Typed: {total_chars}",
                f"Correct Characters: {correct_chars}",
                f"Performance Grade: {grade}"
            ]
            
            for stat in stats:
                c.drawString(90, y_position, stat)
                y_position -= 22
                
            # Performance visualization (simple bar)
            y_position -= 15
            c.setFont("Helvetica-Bold", 14)
            c.drawString(72, y_position, "Performance Summary")
            
            y_position -= 5
            c.line(72, y_position, width - 72, y_position)
            
            y_position -= 30
            
            # WPM bar
            c.setFont("Helvetica", 10)
            c.drawString(90, y_position, "WPM:")
            
            bar_width = min(wpm / 100 * 300, 300)
            c.setFillColor(colors.HexColor("#28a745") if wpm >= 40 else colors.HexColor("#ffc107"))
            c.rect(160, y_position - 5, bar_width, 15, fill=True, stroke=False)
            
            c.setFillColor(colors.black)
            c.drawString(470, y_position, f"{wpm:.1f}")
            
            y_position -= 30
            
            # Accuracy bar
            c.drawString(90, y_position, "Accuracy:")
            
            bar_width = accuracy / 100 * 300
            c.setFillColor(colors.HexColor("#28a745") if accuracy >= 85 else colors.HexColor("#ffc107"))
            c.rect(160, y_position - 5, bar_width, 15, fill=True, stroke=False)
            
            c.setFillColor(colors.black)
            c.drawString(470, y_position, f"{accuracy:.1f}%")
            
            # Key Frequency (if available)
            key_freq = session_data.get('key_frequency', {})
            if key_freq:
                y_position -= 50
                c.setFont("Helvetica-Bold", 14)
                c.drawString(72, y_position, "Most Frequently Used Keys")
                
                y_position -= 5
                c.line(72, y_position, width - 72, y_position)
                
                y_position -= 25
                c.setFont("Helvetica", 11)
                
                # Sort by frequency and get top 10
                sorted_keys = sorted(key_freq.items(), key=lambda x: x[1], reverse=True)[:10]
                
                for key, freq in sorted_keys:
                    c.drawString(90, y_position, f"'{key}': {freq} times")
                    y_position -= 18
                    
            # Footer
            c.setFillColor(colors.HexColor("#666666"))
            c.setFont("Helvetica-Oblique", 9)
            c.drawString(72, 40, "Keyboard Security Monitor - Educational Cybersecurity Tool")
            c.drawString(width - 200, 40, "Page 1 of 1")
            
            # Line separator
            c.setStrokeColor(colors.HexColor("#cccccc"))
            c.setLineWidth(0.5)
            c.line(72, 55, width - 72, 55)
            
            c.save()
            logger.info(f"PDF report generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            return None
            
    def generate_summary_report(self, sessions: List[Dict], 
                                 output_filename: Optional[str] = None) -> Optional[Path]:
        """Generate a summary report for multiple sessions"""
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"typing_summary_{timestamp}.pdf"
            
        filepath = self.output_dir / output_filename
        
        try:
            c = canvas.Canvas(str(filepath), pagesize=letter)
            width, height = letter
            
            # Header
            c.setFillColor(colors.HexColor("#1f538d"))
            c.rect(0, height - 100, width, 100, fill=True, stroke=False)
            
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 24)
            c.drawString(72, height - 60, "Typing Performance Summary")
            
            c.setFont("Helvetica", 12)
            c.drawString(72, height - 85, f"Total Sessions: {len(sessions)}")
            
            # Calculate aggregate stats
            y_position = height - 140
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(72, y_position, "Overall Statistics")
            
            y_position -= 5
            c.setStrokeColor(colors.HexColor("#1f538d"))
            c.setLineWidth(2)
            c.line(72, y_position, width - 72, y_position)
            
            y_position -= 25
            c.setFont("Helvetica", 11)
            
            if sessions:
                avg_wpm = sum(s.get('wpm', 0) for s in sessions) / len(sessions)
                avg_accuracy = sum(s.get('accuracy', 0) for s in sessions) / len(sessions)
                best_wpm = max(s.get('wpm', 0) for s in sessions)
                total_chars = sum(s.get('total_characters', s.get('total_chars', 0)) for s in sessions)
                
                stats = [
                    f"Total Sessions: {len(sessions)}",
                    f"Average WPM: {avg_wpm:.1f}",
                    f"Best WPM: {best_wpm:.1f}",
                    f"Average Accuracy: {avg_accuracy:.1f}%",
                    f"Total Characters Typed: {total_chars:,}"
                ]
                
                for stat in stats:
                    c.drawString(90, y_position, stat)
                    y_position -= 22
                    
            # Footer
            c.setFillColor(colors.HexColor("#666666"))
            c.setFont("Helvetica-Oblique", 9)
            c.drawString(72, 40, "Keyboard Security Monitor - Educational Cybersecurity Tool")
            
            c.save()
            logger.info(f"Summary report generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
            return None
