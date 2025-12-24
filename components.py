from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                             QPushButton, QFrame, QCheckBox, QTableWidget, 
                             QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt, Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class TaskItemWidget(QFrame):
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
        self.title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        if completed:
            self.title_label.setStyleSheet("font-weight: bold; text-decoration: line-through; color: #565F89;")
            
        colors = {"Low": "#9ECE6A", "Medium": "#E0AF68", "High": "#F7768E"}
        p_color = colors.get(priority, "#7AA2F7")
        self.priority_label = QLabel(priority.upper())
        self.priority_label.setStyleSheet(f"font-size: 9px; font-weight: 800; color: {p_color};")
        
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.priority_label)
        
        self.delete_btn = QPushButton("✕")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.setFixedSize(30, 30)
        self.delete_btn.clicked.connect(lambda: self.deleted.emit(self.task_id))
        
        layout.addWidget(self.checkbox)
        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addWidget(self.delete_btn)

class LiveMonitorChart(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, title="Usage", color="#7AA2F7"):
        fig = Figure(figsize=(width, height), dpi=100)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        
        fig.patch.set_facecolor('none')
        self.axes.set_facecolor('none')
        
        self.title_text = title
        self.line_color = color
        self.data = np.zeros(30)
        
        self.axes.set_title(self.title_text, color='#787C99', fontsize=9)
        self.axes.set_ylim(0, 100)
        self.line, = self.axes.plot(self.data, color=self.line_color, linewidth=2)
        self.axes.tick_params(colors='#414868', labelsize=8)
        self.axes.grid(True, color='#24283B', linestyle='--', alpha=0.5)

    def update_data(self, new_val, max_val=100):
        self.data = np.roll(self.data, -1)
        self.data[-1] = new_val
        self.line.set_ydata(self.data)
        if max_val != 100:
            self.axes.set_ylim(0, max(max_val, np.max(self.data) * 1.2))
        self.draw()

    def set_theme(self, dark_mode: bool):
        text_color = '#787C99' if dark_mode else '#4B4F56'
        grid_color = '#24283B' if dark_mode else '#F0F2F5'
        self.axes.set_title(self.title_text, color=text_color)
        self.axes.tick_params(colors=text_color)
        self.axes.grid(True, color=grid_color)
        self.draw()

class ProcessTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Name", "PID", "CPU (%)", "MEM (%)"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)

    def update_processes(self, proc_list):
        self.setRowCount(len(proc_list))
        for i, proc in enumerate(proc_list):
            self.setItem(i, 0, QTableWidgetItem(str(proc['name'])))
            self.setItem(i, 1, QTableWidgetItem(str(proc['pid'])))
            self.setItem(i, 2, QTableWidgetItem(str(proc['cpu_percent'])))
            self.setItem(i, 3, QTableWidgetItem(str(proc['memory_percent'])))
