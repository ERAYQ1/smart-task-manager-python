class StyleManager:
    """
    Advanced Premium Style Engine with Glassmorphism and Fluid Design.
    """
    
    # Modern Color Palette (Tokyo Night / Nord Hybrid)
    COLORS = {
        "bg_dark": "#0B0E14",
        "bg_card": "rgba(25, 27, 38, 0.7)",  # Glass effect
        "bg_sidebar": "#16161E",
        "accent_primary": "#7AA2F7",
        "accent_secondary": "#BB9AF7",
        "accent_success": "#9ECE6A",
        "accent_danger": "#F7768E",
        "accent_warning": "#E0AF68",
        "text_primary": "#C0CAF5",
        "text_secondary": "#565F89",
        "border": "rgba(65, 72, 104, 0.5)",
        "hover": "rgba(122, 162, 247, 0.1)"
    }

    DARK_STYLE = f"""
    QMainWindow {{
        background-color: {COLORS['bg_dark']};
        color: {COLORS['text_primary']};
    }}
    
    QWidget {{
        background: transparent;
        color: {COLORS['text_primary']};
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }}
    
    /* Sidebar Navigation */
    QFrame#sidebar {{
        background-color: {COLORS['bg_sidebar']};
        border-right: 1px solid {COLORS['border']};
    }}
    
    QPushButton#navButton {{
        background: transparent;
        color: {COLORS['text_secondary']};
        text-align: left;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 600;
        border: none;
    }}
    
    QPushButton#navButton:hover {{
        background-color: {COLORS['hover']};
        color: {COLORS['accent_primary']};
    }}
    
    QPushButton#navButton[active="true"] {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {COLORS['accent_primary']}, stop:1 {COLORS['accent_secondary']});
        color: {COLORS['bg_dark']};
    }}
    
    /* Content Cards */
    QFrame#glassCard {{
        background-color: {COLORS['bg_card']};
        border-radius: 12px;
        border: 1px solid {COLORS['border']};
    }}
    
    QLabel#headerTitle {{
        font-size: 24px;
        font-weight: 900;
        color: white;
        letter-spacing: 1px;
    }}
    
    /* Interactive Elements */
    QLineEdit, QComboBox {{
        background-color: rgba(36, 40, 59, 0.8);
        border: 1px solid {COLORS['border']};
        padding: 10px;
        color: white;
        border-radius: 8px;
    }}
    
    QLineEdit:focus {{
        border: 1px solid {COLORS['accent_primary']};
    }}
    
    QPushButton#actionButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['accent_primary']}, stop:1 {COLORS['accent_secondary']});
        color: {COLORS['bg_dark']};
        font-weight: 800;
        padding: 10px 20px;
        border-radius: 8px;
        text-transform: uppercase;
    }}
    
    QPushButton#actionButton:hover {{
        opacity: 0.9;
    }}
    
    /* Task List Aesthetic */
    QListWidget {{
        background: transparent;
        border: none;
    }}
    
    /* Custom Title Bar */
    QFrame#titleBar {{
        background-color: rgba(11, 14, 20, 0.9);
        border-bottom: 1px solid {COLORS['border']};
    }}
    """

    LIGHT_STYLE = """
    /* Premium Light Mode - Minimalist Frost */
    QMainWindow {
        background-color: #F3F4F6;
    }
    QFrame#sidebar {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    QFrame#glassCard {
        background-color: rgba(255, 255, 255, 0.8);
        border: 1px solid #E5E7EB;
        border-radius: 12px;
    }
    /* Rest of light styles follow similar premium logic... */
    """

    @classmethod
    def get_style(cls, dark_mode: bool = True) -> str:
        return cls.DARK_STYLE if dark_mode else cls.LIGHT_STYLE
