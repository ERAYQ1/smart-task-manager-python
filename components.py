from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame, QCheckBox
from PySide6.QtCore import Qt, Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class TaskItemWidget(QFrame):
    """
    Custom widget representating a single task item in the list.
    """
    deleted = Signal(str)
    toggled = Signal(str, bool)

    def __init__(self, task_id: str, title: str, priority: str, completed: bool, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.setObjectName("cardFrame")
        
        layout = QHBoxLayout(self)
        
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(completed)
        self.checkbox.stateChanged.connect(lambda state: self.toggled.emit(self.task_id, state == Qt.Checked.value))
        
        title_layout = QVBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold;")
        if completed:
            self.title_label.setStyleSheet("font-weight: bold; text-decoration: line-through; color: gray;")
            
        self.priority_label = QLabel(f"Priority: {priority}")
        self.priority_label.setStyleSheet("font-size: 10px; color: #888;")
        
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.priority_label)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.setFixedWidth(60)
        self.delete_btn.clicked.connect(lambda: self.deleted.emit(self.task_id))
        
        layout.addWidget(self.checkbox)
        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addWidget(self.delete_btn)

class LiveMonitorChart(FigureCanvas):
    """
    Matplotlib canvas for real-time system resource monitoring.
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100, title="CPU Usage"):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        
        fig.patch.set_facecolor('none')
        self.axes.set_facecolor('none')
        
        self.title = title
        self.data = np.zeros(20)
        self.axes.set_title(self.title, color='gray')
        self.axes.set_ylim(0, 100)
        self.line, = self.axes.plot(self.data, color='#BB86FC' if "CPU" in title else '#03DAC6')
        self.axes.tick_params(colors='gray')
        
    def update_data(self, new_val):
        """Adds a new data point and updates the plot."""
        self.data = np.roll(self.data, -1)
        self.data[-1] = new_val
        self.line.set_ydata(self.data)
        self.draw()

    def set_theme(self, dark_mode: bool):
        """Updates chart colors based on the theme."""
        color = '#BB86FC' if dark_mode else '#6200EE'
        text_color = '#E0E0E0' if dark_mode else '#212121'
        self.line.set_color(color)
        self.axes.set_title(self.title, color=text_color)
        self.axes.tick_params(colors=text_color)
        self.draw()
