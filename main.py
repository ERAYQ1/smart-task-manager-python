import sys
from PySide6.QtWidgets import QApplication
from gui import SmartTaskManagerUI

def main():
    """
    Application entry point.
    """
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setStyle("Fusion")
    
    window = SmartTaskManagerUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
