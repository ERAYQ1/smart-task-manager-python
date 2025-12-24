import uuid
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, 
                             QListWidget, QListWidgetItem, QTabWidget, QFrame)
from PySide6.QtCore import QTimer, Qt
from data_manager import DataManager
from system_monitor import SystemMonitor
from styles import StyleManager
from components import TaskItemWidget, LiveMonitorChart

class SmartTaskManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Task Manager & System Monitor")
        self.resize(800, 600)
        
        self.data_manager = DataManager()
        self.system_monitor = SystemMonitor()
        self.dark_mode = True
        
        self._init_ui()
        self._load_tasks_into_list()
        self._apply_style()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_system_metrics)
        self.timer.start(1000)

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        
        header_layout = QHBoxLayout()
        self.title_label = QLabel("Smart Task Manager")
        self.title_label.setObjectName("titleLabel")
        
        self.theme_btn = QPushButton("Toggle Theme")
        self.theme_btn.clicked.connect(self._toggle_theme)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_btn)
        self.main_layout.addLayout(header_layout)
        
        self.tabs = QTabWidget()
        self.task_tab = QWidget()
        self.monitor_tab = QWidget()
        
        self.tabs.addTab(self.task_tab, "Tasks")
        self.tabs.addTab(self.monitor_tab, "System Monitor")
        self.main_layout.addWidget(self.tabs)
        
        self._setup_task_tab()
        self._setup_monitor_tab()

    def _setup_task_tab(self):
        layout = QVBoxLayout(self.task_tab)
        
        input_frame = QFrame()
        input_frame.setObjectName("cardFrame")
        input_layout = QHBoxLayout(input_frame)
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        
        self.add_btn = QPushButton("Add Task")
        self.add_btn.clicked.connect(self._add_task)
        
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.priority_combo)
        input_layout.addWidget(self.add_btn)
        layout.addWidget(input_frame)
        
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

    def _setup_monitor_tab(self):
        layout = QVBoxLayout(self.monitor_tab)
        
        self.cpu_chart = LiveMonitorChart(title="CPU Usage (%)")
        self.ram_chart = LiveMonitorChart(title="RAM Usage (%)")
        
        layout.addWidget(self.cpu_chart)
        layout.addWidget(self.ram_chart)
        
        self.metrics_label = QLabel("Loading metrics...")
        layout.addWidget(self.metrics_label)

    def _add_task(self):
        title = self.task_input.text().strip()
        if not title:
            return
            
        task_id = str(uuid.uuid4())
        priority = self.priority_combo.currentText()
        
        task = {
            "id": task_id,
            "title": title,
            "priority": priority,
            "completed": False
        }
        
        self.data_manager.add_task(task)
        self._add_task_widget(task)
        self.task_input.clear()

    def _add_task_widget(self, task):
        item = QListWidgetItem(self.task_list)
        widget = TaskItemWidget(task['id'], task['title'], task['priority'], task['completed'])
        
        widget.deleted.connect(self._delete_task)
        widget.toggled.connect(self._toggle_task_status)
        
        item.setSizeHint(widget.sizeHint())
        self.task_list.addItem(item)
        self.task_list.setItemWidget(item, widget)

    def _load_tasks_into_list(self):
        self.task_list.clear()
        tasks = self.data_manager.load_tasks()
        for task in tasks:
            self._add_task_widget(task)

    def _delete_task(self, task_id):
        self.data_manager.delete_task(task_id)
        self._load_tasks_into_list()

    def _toggle_task_status(self, task_id, completed):
        tasks = self.data_manager.load_tasks()
        for task in tasks:
            if task['id'] == task_id:
                task['completed'] = completed
                self.data_manager.update_task(task)
                break
        self._load_tasks_into_list()

    def _toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self._apply_style()
        self.cpu_chart.set_theme(self.dark_mode)
        self.ram_chart.set_theme(self.dark_mode)

    def _apply_style(self):
        self.setStyleSheet(StyleManager.get_style(self.dark_mode))

    def _update_system_metrics(self):
        metrics = self.system_monitor.get_all_metrics()
        
        self.cpu_chart.update_data(metrics['cpu'])
        self.ram_chart.update_data(metrics['memory']['percent'])
        
        text = (f"CPU: {metrics['cpu']}% | "
                f"RAM: {metrics['memory']['percent']}% ({metrics['memory']['available']}GB free) | "
                f"Disk: {metrics['disk']['percent']}% ({metrics['disk']['used']}GB used)")
        self.metrics_label.setText(text)
