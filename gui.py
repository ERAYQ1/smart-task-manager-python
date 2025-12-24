import uuid
import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, 
                             QListWidget, QListWidgetItem, QTabWidget, QFrame,
                             QSystemTrayIcon, QMenu, QApplication)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QTimer, Qt
from data_manager import DataManager
from system_monitor import SystemMonitor
from styles import StyleManager
from components import TaskItemWidget, LiveMonitorChart, ProcessTable

class SmartTaskManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Task Manager Pro")
        self.resize(1000, 700)
        
        self.data_manager = DataManager()
        self.system_monitor = SystemMonitor()
        self.dark_mode = True
        self.proc_update_counter = 0
        
        self._init_ui()
        self._setup_tray()
        self._load_tasks_into_list()
        self._apply_style()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_all)
        self.timer.start(1000)

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        header_layout = QHBoxLayout()
        self.title_label = QLabel("SYSTEM CONTROL")
        self.title_label.setObjectName("titleLabel")
        
        self.theme_btn = QPushButton("◑")
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.clicked.connect(self._toggle_theme)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_btn)
        self.main_layout.addLayout(header_layout)
        
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        self.task_tab = QWidget()
        self.monitor_tab = QWidget()
        self.process_tab = QWidget()
        
        self.tabs.addTab(self.task_tab, "TASKS")
        self.tabs.addTab(self.monitor_tab, "MONITOR")
        self.tabs.addTab(self.process_tab, "PROCESSES")
        
        self._setup_task_tab()
        self._setup_monitor_tab()
        self._setup_process_tab()

    def _setup_task_tab(self):
        layout = QVBoxLayout(self.task_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        input_frame = QFrame()
        input_frame.setObjectName("cardFrame")
        input_layout = QHBoxLayout(input_frame)
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Describe your next task...")
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setFixedWidth(120)
        
        self.add_btn = QPushButton("ADD")
        self.add_btn.clicked.connect(self._add_task)
        
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.priority_combo)
        input_layout.addWidget(self.add_btn)
        layout.addWidget(input_frame)
        
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

    def _setup_monitor_tab(self):
        layout = QVBoxLayout(self.monitor_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        charts_layout = QHBoxLayout()
        self.cpu_chart = LiveMonitorChart(title="CPU LOAD (%)", color="#BB9AF7")
        self.ram_chart = LiveMonitorChart(title="MEMORY USAGE (%)", color="#7AA2F7")
        charts_layout.addWidget(self.cpu_chart)
        charts_layout.addWidget(self.ram_chart)
        layout.addLayout(charts_layout)
        
        net_layout = QHBoxLayout()
        self.net_up_chart = LiveMonitorChart(title="NET UPLOAD (KB/s)", color="#F7768E")
        self.net_down_chart = LiveMonitorChart(title="NET DOWNLOAD (KB/s)", color="#9ECE6A")
        net_layout.addWidget(self.net_up_chart)
        net_layout.addWidget(self.net_down_chart)
        layout.addLayout(net_layout)
        
        self.metrics_label = QLabel("Initializing metrics...")
        self.metrics_label.setStyleSheet("font-family: 'Consolas'; font-size: 11px; color: #565F89;")
        layout.addWidget(self.metrics_label)

    def _setup_process_tab(self):
        layout = QVBoxLayout(self.process_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        self.proc_table = ProcessTable()
        layout.addWidget(self.proc_table)
        
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("FORCE REFRESH")
        self.refresh_btn.clicked.connect(self._update_processes)
        btn_layout.addStretch()
        btn_layout.addWidget(self.refresh_btn)
        layout.addLayout(btn_layout)

    def _setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QSystemTrayIcon.MessageIcon))
        
        tray_menu = QMenu()
        show_action = QAction("Show Window", self)
        show_action.triggered.connect(self.showNormal)
        quit_action = QAction("Exit App", self)
        quit_action.triggered.connect(QApplication.quit)
        
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def _add_task(self):
        title = self.task_input.text().strip()
        if not title: return
        task = {"id": str(uuid.uuid4()), "title": title, "priority": self.priority_combo.currentText(), "completed": False}
        self.data_manager.add_task(task)
        self._load_tasks_into_list()
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
        for task in self.data_manager.load_tasks():
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
        for chart in [self.cpu_chart, self.ram_chart, self.net_up_chart, self.net_down_chart]:
            chart.set_theme(self.dark_mode)

    def _apply_style(self):
        self.setStyleSheet(StyleManager.get_style(self.dark_mode))

    def _update_all(self):
        self._update_system_metrics()
        
        if self.tabs.currentIndex() == 2:
            self.proc_update_counter += 1
            if self.proc_update_counter >= 3:
                self._update_processes()
                self.proc_update_counter = 0
        else:
            self.proc_update_counter = 0

    def _update_system_metrics(self):
        metrics = self.system_monitor.get_all_metrics()
        self.cpu_chart.update_data(metrics['cpu'])
        self.ram_chart.update_data(metrics['memory']['percent'])
        self.net_up_chart.update_data(metrics['network']['sent'], max_val=500)
        self.net_down_chart.update_data(metrics['network']['recv'], max_val=500)
        
        text = (f"CPU: {metrics['cpu']}% | RAM: {metrics['memory']['percent']}% | "
                f"UP: {metrics['network']['sent']}KB/s | DOWN: {metrics['network']['recv']}KB/s")
        self.metrics_label.setText(text)

    def _update_processes(self):
        procs = self.system_monitor.get_processes()
        self.proc_table.update_processes(procs)

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()
