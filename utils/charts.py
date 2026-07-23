"""
Charts Module
Handles data visualization using matplotlib
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from typing import List, Dict

class ChartManager:
    """Manages chart creation and display"""
    
    def __init__(self):
        self.figures = []
        
    def create_wpm_chart(self, parent, sessions: List[Dict]):
        """Create WPM trend chart"""
        if not sessions:
            return None
            
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Extract data
        dates = [s.get('session_date', '') for s in sessions]
        wpm_values = [s.get('wpm', 0) for s in sessions]
        
        # Plot
        ax.plot(range(len(dates)), wpm_values, marker='o', linewidth=2, markersize=6)
        ax.set_xlabel('Session')
        ax.set_ylabel('WPM')
        ax.set_title('Words Per Minute Trend')
        ax.grid(True, alpha=0.3)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        self.figures.append(fig)
        return canvas
        
    def create_accuracy_chart(self, parent, sessions: List[Dict]):
        """Create accuracy trend chart"""
        if not sessions:
            return None
            
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Extract data
        dates = [s.get('session_date', '') for s in sessions]
        accuracy_values = [s.get('accuracy', 0) for s in sessions]
        
        # Plot
        ax.bar(range(len(dates)), accuracy_values, color='green', alpha=0.7)
        ax.set_xlabel('Session')
        ax.set_ylabel('Accuracy (%)')
        ax.set_title('Accuracy Trend')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        self.figures.append(fig)
        return canvas
        
    def create_key_frequency_chart(self, parent, key_freq: Dict[str, int]):
        """Create key frequency chart"""
        if not key_freq:
            return None
            
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Sort by frequency
        sorted_keys = sorted(key_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        keys = [k for k, v in sorted_keys]
        freqs = [v for k, v in sorted_keys]
        
        # Plot
        ax.barh(keys, freqs, color='steelblue', alpha=0.7)
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Key')
        ax.set_title('Top 10 Most Used Keys')
        ax.invert_yaxis()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        self.figures.append(fig)
        return canvas
        
    def clear_figures(self):
        """Clear all figures"""
        for fig in self.figures:
            plt.close(fig)
        self.figures.clear()
