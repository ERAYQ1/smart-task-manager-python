class StyleManager:
    """
    Centralized manager for Dark and Light mode QSS (Qt Style Sheets).
    """

    DARK_STYLE = """
    QMainWindow {
        background-color: #121212;
        color: #E0E0E0;
    }
    QWidget {
        background-color: #1E1E1E;
        color: #E0E0E0;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton {
        background-color: #333333;
        color: white;
        border: 1px solid #444444;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #444444;
    }
    QPushButton#dangerButton {
        background-color: #CF6679;
        color: #000000;
    }
    QPushButton#dangerButton:hover {
        background-color: #D32F2F;
    }
    QLineEdit, QComboBox, QTextEdit {
        background-color: #2D2D2D;
        border: 1px solid #444444;
        padding: 6px;
        color: white;
        border-radius: 4px;
    }
    QLabel {
        color: #E0E0E0;
        font-size: 14px;
    }
    QLabel#titleLabel {
        font-size: 24px;
        font-weight: bold;
        color: #BB86FC;
    }
    QListWidget {
        background-color: #1E1E1E;
        border: none;
    }
    QFrame#cardFrame {
        background-color: #2D2D2D;
        border-radius: 8px;
        border: 1px solid #333333;
    }
    """

    LIGHT_STYLE = """
    QMainWindow {
        background-color: #F5F5F5;
        color: #212121;
    }
    QWidget {
        background-color: #FFFFFF;
        color: #212121;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton {
        background-color: #E0E0E0;
        color: #212121;
        border: 1px solid #BDBDBD;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #D5D5D5;
    }
    QPushButton#dangerButton {
        background-color: #D32F2F;
        color: white;
    }
    QPushButton#dangerButton:hover {
        background-color: #B71C1C;
    }
    QLineEdit, QComboBox, QTextEdit {
        background-color: #FFFFFF;
        border: 1px solid #BDBDBD;
        padding: 6px;
        color: #212121;
        border-radius: 4px;
    }
    QLabel {
        color: #212121;
        font-size: 14px;
    }
    QLabel#titleLabel {
        font-size: 24px;
        font-weight: bold;
        color: #6200EE;
    }
    QListWidget {
        background-color: #FFFFFF;
        border: none;
    }
    QFrame#cardFrame {
        background-color: #F9F9F9;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
    }
    """

    @classmethod
    def get_style(cls, dark_mode: bool = True) -> str:
        """Returns the requested style sheet."""
        return cls.DARK_STYLE if dark_mode else cls.LIGHT_STYLE
