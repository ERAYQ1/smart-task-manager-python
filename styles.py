class StyleManager:
    DARK_STYLE = """
    QMainWindow {
        background-color: #0F0F13;
        color: #FFFFFF;
    }
    QWidget {
        background-color: #16161E;
        color: #A9B1D6;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    QTabWidget::pane {
        border: 1px solid #24283B;
        background: #1A1B26;
        border-radius: 8px;
    }
    QTabBar::tab {
        background: #1A1B26;
        color: #787C99;
        padding: 10px 20px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background: #24283B;
        color: #7AA2F7;
        border-bottom: 2px solid #7AA2F7;
    }
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7AA2F7, stop:1 #2AC3DE);
        color: #1A1B26;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 800;
        text-transform: uppercase;
        font-size: 11px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #89B4FA, stop:1 #3BD1ED);
    }
    QPushButton#dangerButton {
        background: #F7768E;
        color: #1A1B26;
    }
    QPushButton#dangerButton:hover {
        background: #FF8A9F;
    }
    QLineEdit, QComboBox, QTextEdit {
        background-color: #24283B;
        border: 1px solid #414868;
        padding: 8px;
        color: #C0CAF5;
        border-radius: 6px;
    }
    QLabel#titleLabel {
        font-size: 28px;
        font-weight: 900;
        color: #BB9AF7;
        margin-bottom: 10px;
    }
    QListWidget {
        background-color: #1A1B26;
        border: 1px solid #24283B;
        border-radius: 8px;
        padding: 5px;
    }
    QFrame#cardFrame {
        background-color: #24283B;
        border-radius: 10px;
        border: 1px solid #414868;
        padding: 5px;
    }
    QHeaderView::section {
        background-color: #1A1B26;
        color: #7AA2F7;
        padding: 5px;
        border: none;
        font-weight: bold;
    }
    """

    LIGHT_STYLE = """
    QMainWindow {
        background-color: #F0F2F5;
        color: #1C1E21;
    }
    QWidget {
        background-color: #FFFFFF;
        color: #4B4F56;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    QTabWidget::pane {
        border: 1px solid #DADDE1;
        background: #FFFFFF;
        border-radius: 8px;
    }
    QTabBar::tab {
        background: #EBEDF0;
        color: #606770;
        padding: 10px 20px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }
    QTabBar::tab:selected {
        background: #FFFFFF;
        color: #1877F2;
        border-bottom: 2px solid #1877F2;
    }
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1877F2, stop:1 #21AFFD);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 11px;
    }
    QPushButton#dangerButton {
        background: #FA3E3E;
    }
    QLineEdit, QComboBox, QTextEdit {
        background-color: #F5F6F7;
        border: 1px solid #CCD0D5;
        padding: 8px;
        color: #1C1E21;
        border-radius: 6px;
    }
    QLabel#titleLabel {
        font-size: 28px;
        font-weight: bold;
        color: #1877F2;
    }
    QFrame#cardFrame {
        background-color: #F0F2F5;
        border-radius: 10px;
        border: 1px solid #EBEDF0;
    }
    """

    @classmethod
    def get_style(cls, dark_mode: bool = True) -> str:
        return cls.DARK_STYLE if dark_mode else cls.LIGHT_STYLE
