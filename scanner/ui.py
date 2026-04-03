"""Minimal Tkinter UI for displaying malware scan results."""
import tkinter as tk
from tkinter import messagebox, font
import json


def show_scan_result(verdict: dict):
    """
    Display scan results in a GUI popup window.
    
    Args:
        verdict: Dictionary containing scan results with keys:
                 - file_hash: SHA-256 hash of the file
                 - known_malware: boolean
                 - malware_name: name if detected
                 - malware_family: family if detected  
                 - detection_method: how it was detected
                 - analysis_result: heuristic analysis if performed
    """
    # Create hidden root window (we only want the popup, not a main window)
    root = tk.Tk()
    root.withdraw()
    
    # Extract verdict info
    is_malware = verdict.get("known_malware", False)
    method = verdict.get("detection_method", "Unknown")
    file_hash = verdict.get("file_hash", "N/A")
    
    # Build title and message
    if is_malware:
        title = "⚠️  MALWARE DETECTED"
        malware_name = verdict.get("malware_name", "Unknown")
        malware_family = verdict.get("malware_family", "Unknown")
        message = (
            f"Risk Level: HIGH\n\n"
            f"Malware Name: {malware_name}\n"
            f"Family: {malware_family}\n\n"
            f"Detection Method: {method}\n"
            f"File Hash: {file_hash[:16]}...\n\n"
            f"⚠️  This file is known malware."
        )
        # Use showwarning for malware
        messagebox.showwarning(title, message)
    else:
        title = "✓ SCAN COMPLETE"
        message = (
            f"Risk Level: LOW\n\n"
            f"Detection Method: {method}\n"
            f"File Hash: {file_hash[:16]}...\n\n"
            f"✓ No known malware detected."
        )
        # Use showinfo for clean files
        messagebox.showinfo(title, message)
    
    root.destroy()


def show_error(error_message: str):
    """Display an error message in a popup window."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Scan Error", f"Error during scan:\n\n{error_message}")
    root.destroy()


def show_scanning():
    """Show a non-blocking scanning message."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Scanning", "Scan in progress...\nPlease wait.")
    root.destroy()
