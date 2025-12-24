from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                             QPushButton, QFrame, QCheckBox, QTableWidget, 
                             QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPainter, QLinearGradient
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class TaskItemWidget(QFrame):
    deleted = Signal(str)
    toggled = Signal(str, bool)
    edited = Signal(str, str)

    def __init__(self, task_id: str, title: str, priority: str, completed: bool, dark_mode: bool = True, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.priority = priority
        self.dark_mode = dark_mode
        self.setObjectName("glassCard")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(completed)
        self.checkbox.stateChanged.connect(lambda state: self.toggled.emit(self.task_id, state == Qt.Checked.value))
        
        title_layout = QVBoxLayout()
        self.title_label = QLabel(title)
        
        self.priority_label = QLabel(priority.upper())
        
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.priority_label)
        
        self.edit_btn = QPushButton("✎")
        self.edit_btn.setFixedSize(32, 32)
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.clicked.connect(self._on_edit)
        
        self.delete_btn = QPushButton("✕")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.setFixedSize(32, 32)
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.clicked.connect(lambda: self.deleted.emit(self.task_id))
        
        layout.addWidget(self.checkbox)
        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.delete_btn)
        self._apply_internal_styles(completed)

    def _on_edit(self):
        from PySide6.QtWidgets import QInputDialog
        new_title, ok = QInputDialog.getText(self, "Edit Task", "Task Name:", text=self.title_label.text())
        if ok and new_title.strip():
            self.edited.emit(self.task_id, new_title.strip())

    def _apply_internal_styles(self, completed: bool):
        if completed:
            color = "#565F89" if self.dark_mode else "#90949C"
            self.title_label.setStyleSheet(f"font-weight: 700; font-size: 14px; text-decoration: line-through; color: {color};")
        else:
            color = "#C0CAF5" if self.dark_mode else "#1C1E21"
            self.title_label.setStyleSheet(f"font-weight: 700; font-size: 14px; color: {color};")
            
        dark_colors = {"Low": "#9ECE6A", "Medium": "#E0AF68", "High": "#F7768E"}
        light_colors = {"Low": "#28A745", "Medium": "#D39E00", "High": "#DC3545"}
        p_color = (dark_colors if self.dark_mode else light_colors).get(self.priority, "#7AA2F7")
        self.priority_label.setStyleSheet(f"font-size: 10px; font-weight: 900; color: {p_color}; letter-spacing: 0.5px;")

    def update_state(self, completed: bool, dark_mode: bool):
        self.dark_mode = dark_mode
        self._apply_internal_styles(completed)

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
        self.data = np.zeros(40)
        
        self.axes.set_title(self.title_text, color='#787C99', fontsize=10, fontweight='bold', pad=15)
        self.axes.set_ylim(0, 105)
        self.line, = self.axes.plot(self.data, color=self.line_color, linewidth=2.5, antialiased=True)
        self.fill = self.axes.fill_between(range(len(self.data)), self.data, color=self.line_color, alpha=0.15)
        
        self.axes.tick_params(colors='#414868', labelsize=8)
        self.axes.grid(True, color='#24283B', linestyle=':', alpha=0.3)
        for spine in self.axes.spines.values():
            spine.set_visible(False)
        fig.tight_layout()

    def update_data(self, new_val, max_val=100):
        try:
            self.data = np.roll(self.data, -1)
            self.data[-1] = new_val
            
            self.line.set_ydata(self.data)
            
            # Update fill
            self.fill.remove()
            self.fill = self.axes.fill_between(range(len(self.data)), self.data, color=self.line_color, alpha=0.15)
            
            if max_val != 100:
                current_max = np.max(self.data)
                self.axes.set_ylim(0, max(max_val, current_max * 1.3))
            
            self.draw_idle()
        except Exception:
            pass

    def set_theme(self, dark_mode: bool):
        text_color = '#787C99' if dark_mode else '#4B4F56'
        grid_color = '#24283B' if dark_mode else '#E5E7EB'
        self.axes.set_title(self.title_text, color=text_color)
        self.axes.tick_params(colors=text_color)
        self.axes.grid(True, color=grid_color)
        self.draw_idle()

class ProcessTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["NAME", "PID", "CPU %", "MEM %"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStyleSheet("font-weight: bold; text-transform: uppercase; font-size: 10px;")
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setStyleSheet("QTableWidget { border: none; background: transparent; }")

    def update_processes(self, proc_list):
        self.setRowCount(len(proc_list))
        for i, proc in enumerate(proc_list):
            for col, val in enumerate([proc['name'], proc['pid'], proc['cpu_percent'], proc['memory_percent']]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, col, item)
