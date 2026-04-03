"""Professional Tkinter UI for displaying detailed malware scan results."""
import tkinter as tk
from tkinter import font as tkfont
import os


def _get_risk_color(risk_percentage):
    """Return color based on risk percentage: green (0%), yellow (25-50%), red (70%+)."""
    if risk_percentage == 0:
        return "#2ecc71"  # Green
    elif risk_percentage < 25:
        return "#f39c12"  # Orange
    elif risk_percentage < 50:
        return "#f39c12"  # Orange
    elif risk_percentage < 70:
        return "#e74c3c"  # Red
    else:
        return "#c0392b"  # Dark red


def _get_risk_label(risk_percentage):
    """Return risk level label based on percentage."""
    if risk_percentage == 0:
        return "NONE"
    elif risk_percentage < 25:
        return "LOW"
    elif risk_percentage < 50:
        return "MEDIUM"
    elif risk_percentage < 70:
        return "HIGH"
    else:
        return "CRITICAL"


def show_scan_result(verdict: dict):
    """
    Display detailed scan results in a professional custom window.
    
    Args:
        verdict: Dictionary containing scan results with keys:
                 - file_path: path to scanned file
                 - file_hash: SHA-256 hash
                 - known_malware: boolean
                 - malware_name/family: if detected
                 - detection_method: how detected
                 - analysis_result: heuristic analysis (contains capabilities, risk_percentage)
    """
    # Create main window
    root = tk.Tk()
    root.title("CYBERTRACKER - Scan Results")
    root.geometry("700x600")
    root.resizable(False, False)
    
    # Extract verdict data
    file_path = verdict.get("file_path", "Unknown")
    file_hash = verdict.get("file_hash", "N/A")
    is_malware = verdict.get("known_malware", False)
    detection_method = verdict.get("detection_method", "Unknown")
    
    # Calculate risk
    if is_malware:
        risk_percentage = 100
        risk_level = "CRITICAL"
        capabilities = []
    else:
        analysis = verdict.get("analysis_result", {})
        if analysis is None:
            analysis = {}
        risk_percentage = analysis.get("risk_percentage", 0)
        risk_level = _get_risk_label(risk_percentage)
        capabilities = analysis.get("capabilities", [])
    
    risk_color = _get_risk_color(risk_percentage)
    
    # Configure fonts
    title_font = tkfont.Font(family="Arial", size=14, weight="bold")
    header_font = tkfont.Font(family="Arial", size=11, weight="bold")
    normal_font = tkfont.Font(family="Arial", size=10)
    mono_font = tkfont.Font(family="Courier", size=9)
    
    # --- TOP SECTION: Risk Bar ---
    top_frame = tk.Frame(root, bg=risk_color, height=80)
    top_frame.pack(fill=tk.X, padx=0, pady=0)
    top_frame.pack_propagate(False)
    
    risk_title = f"{'⚠️  MALWARE DETECTED' if is_malware else '✓ SCAN COMPLETE'}"
    risk_text = f"{risk_level} Risk - {risk_percentage}%"
    
    tk.Label(
        top_frame,
        text=risk_title,
        font=tkfont.Font(family="Arial", size=16, weight="bold"),
        bg=risk_color,
        fg="white"
    ).pack(pady=(10, 5))
    
    tk.Label(
        top_frame,
        text=risk_text,
        font=tkfont.Font(family="Arial", size=13, weight="bold"),
        bg=risk_color,
        fg="white"
    ).pack(pady=(0, 10))
    
    # --- CONTENT SECTION: Scrollable frame ---
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    # File path
    tk.Label(
        content_frame,
        text="File Path:",
        font=header_font,
        bg="white",
        fg="#2c3e50"
    ).pack(anchor=tk.W, pady=(0, 3))
    
    file_label = tk.Label(
        content_frame,
        text=file_path,
        font=mono_font,
        bg="#ecf0f1",
        fg="#2c3e50",
        wraplength=650,
        justify=tk.LEFT,
        relief=tk.FLAT,
        padx=10,
        pady=8
    )
    file_label.pack(anchor=tk.W, fill=tk.X, pady=(0, 12))
    
    # File hash
    tk.Label(
        content_frame,
        text="File Hash (SHA-256):",
        font=header_font,
        bg="white",
        fg="#2c3e50"
    ).pack(anchor=tk.W, pady=(0, 3))
    
    hash_display = f"{file_hash[:32]}..." if len(file_hash) > 32 else file_hash
    tk.Label(
        content_frame,
        text=hash_display,
        font=mono_font,
        bg="#ecf0f1",
        fg="#7f8c8d",
        padx=10,
        pady=6,
        relief=tk.FLAT
    ).pack(anchor=tk.W, fill=tk.X, pady=(0, 12))
    
    # Detection method
    tk.Label(
        content_frame,
        text="Detection Method:",
        font=header_font,
        bg="white",
        fg="#2c3e50"
    ).pack(anchor=tk.W, pady=(0, 3))
    
    tk.Label(
        content_frame,
        text=detection_method,
        font=normal_font,
        bg="white",
        fg="#34495e"
    ).pack(anchor=tk.W, pady=(0, 12))
    
    # Malware info (if detected)
    if is_malware:
        tk.Label(
            content_frame,
            text="Threat Information:",
            font=header_font,
            bg="white",
            fg="#2c3e50"
        ).pack(anchor=tk.W, pady=(0, 3))
        
        malware_name = verdict.get("malware_name", "Unknown")
        malware_family = verdict.get("malware_family", "Unknown")
        
        info_text = f"Name: {malware_name}\nFamily: {malware_family}"
        tk.Label(
            content_frame,
            text=info_text,
            font=normal_font,
            bg="white",
            fg="#e74c3c",
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(0, 12))
    
    # Capabilities (if analyzed)
    if capabilities:
        tk.Label(
            content_frame,
            text="Detected Capabilities:",
            font=header_font,
            bg="white",
            fg="#2c3e50"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        cap_text = "\n".join([f"• {cap.replace('_', ' ').title()}" for cap in capabilities])
        tk.Label(
            content_frame,
            text=cap_text,
            font=normal_font,
            bg="white",
            fg="#34495e",
            justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(0, 12))
    
    # Recommended action
    action_color = "#c0392b" if is_malware or risk_percentage >= 70 else "#2ecc71"
    action_text = "QUARANTINE IMMEDIATELY" if (is_malware or risk_percentage >= 70) else "File appears safe"
    
    tk.Label(
        content_frame,
        text="Recommended Action:",
        font=header_font,
        bg="white",
        fg="#2c3e50"
    ).pack(anchor=tk.W, pady=(5, 3))
    
    tk.Label(
        content_frame,
        text=action_text,
        font=tkfont.Font(family="Arial", size=11, weight="bold"),
        bg=action_color,
        fg="white",
        padx=12,
        pady=10,
        relief=tk.FLAT
    ).pack(anchor=tk.W, fill=tk.X, pady=(0, 0))
    
    # --- BOTTOM SECTION: Close Button ---
    button_frame = tk.Frame(root, bg="white")
    button_frame.pack(fill=tk.X, padx=15, pady=15)
    
    close_btn = tk.Button(
        button_frame,
        text="Close",
        font=normal_font,
        bg="#34495e",
        fg="white",
        width=20,
        padx=15,
        pady=10,
        relief=tk.FLAT,
        cursor="hand2",
        command=root.destroy
    )
    close_btn.pack(side=tk.RIGHT)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Show window
    root.mainloop()


def show_error(error_message: str):
    """Display an error message in a popup window."""
    root = tk.Tk()
    root.title("CYBERTRACKER - Error")
    root.geometry("500x200")
    root.resizable(False, False)
    
    # Error colors
    root.configure(bg="#fff3cd")
    
    title_font = tkfont.Font(family="Arial", size=12, weight="bold")
    normal_font = tkfont.Font(family="Arial", size=10)
    
    tk.Label(
        root,
        text="❌ Scan Error",
        font=title_font,
        bg="#f39c12",
        fg="white"
    ).pack(fill=tk.X, padx=0, pady=0)
    
    error_frame = tk.Frame(root, bg="white")
    error_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    tk.Label(
        error_frame,
        text=error_message,
        font=normal_font,
        bg="white",
        fg="#2c3e50",
        wraplength=450,
        justify=tk.LEFT
    ).pack(anchor=tk.W, pady=(0, 15))
    
    tk.Button(
        error_frame,
        text="Close",
        font=normal_font,
        bg="#34495e",
        fg="white",
        padx=15,
        pady=8,
        relief=tk.FLAT,
        cursor="hand2",
        command=root.destroy
    ).pack(side=tk.RIGHT)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()
