import uuid
import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, 
                             QListWidget, QListWidgetItem, QStackedWidget, QFrame,
                             QSystemTrayIcon, QMenu, QApplication, QStyle, QGraphicsDropShadowEffect)
from PySide6.QtGui import QIcon, QAction, QColor, QMouseEvent
from PySide6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QPoint
from data_manager import DataManager
from system_monitor import SystemMonitor
from styles import StyleManager
from components import TaskItemWidget, LiveMonitorChart, ProcessTable

class SmartTaskManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Task Manager Pro")
        self.resize(1100, 750)
        
        # Remove standard frame for "Wow" factor
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.data_manager = DataManager()
        self.system_monitor = SystemMonitor()
        self.dark_mode = True
        self.proc_update_counter = 0
        self._drag_pos = QPoint()
        
        self._init_ui()
        self._setup_tray()
        self._load_tasks_into_list()
        self._apply_style()
        self._apply_shadow()
        
        # Default page
        self._switch_page(0)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_all)
        self.timer.start(1000)

    def _init_ui(self):
        # Main background container for transparency
        self.main_container = QFrame()
        self.main_container.setObjectName("glassCard")
        self.setCentralWidget(self.main_container)
        
        self.outer_layout = QVBoxLayout(self.main_container)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)
        
        # Custom Title Bar
        self.title_bar = QFrame()
        self.title_bar.setObjectName("titleBar")
        self.title_bar.setFixedHeight(50)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(20, 0, 10, 0)
        
        self.app_title = QLabel("SYSTEM CONTROL <b>PRO</b>")
        self.app_title.setObjectName("headerTitle")
        
        self.btn_min = QPushButton("–")
        self.btn_close = QPushButton("✕")
        for btn in [self.btn_min, self.btn_close]:
            btn.setFixedSize(30, 30)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("background: transparent; border: none; font-size: 16px; color: #565F89;")
        
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_close.clicked.connect(self.close)
        
        title_layout.addWidget(self.app_title)
        title_layout.addStretch()
        title_layout.addWidget(self.btn_min)
        title_layout.addWidget(self.btn_close)
        self.outer_layout.addWidget(self.title_bar)
        
        # Content Area with Sidebar
        self.content_container = QWidget()
        self.inner_layout = QHBoxLayout(self.content_container)
        self.inner_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(240)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(15, 30, 15, 30)
        self.sidebar_layout.setSpacing(10)
        
        # Navigation Buttons
        self.nav_btns = []
        menus = [("TASKS", 0), ("MONITOR", 1), ("PROCESSES", 2)]
        for text, index in menus:
            btn = QPushButton(text)
            btn.setObjectName("navButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=index: self._switch_page(idx))
            self.sidebar_layout.addWidget(btn)
            self.nav_btns.append(btn)
            
        self.sidebar_layout.addStretch()
        
        self.theme_btn = QPushButton("Toggle Theme")
        self.theme_btn.setObjectName("navButton")
        self.theme_btn.clicked.connect(self._toggle_theme)
        self.sidebar_layout.addWidget(self.theme_btn)
        
        self.inner_layout.addWidget(self.sidebar)
        
        # Main Work Area
        self.stack = QStackedWidget()
        self.inner_layout.addWidget(self.stack)
        
        self._setup_task_page()
        self._setup_monitor_page()
        self._setup_process_page()
        
        self.outer_layout.addWidget(self.content_container)

    def _setup_task_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        input_frame = QFrame()
        input_frame.setObjectName("glassCard")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 15, 15, 15)
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Describe your next professional goal...")
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setFixedWidth(130)
        
        self.add_btn = QPushButton("ADD TASK")
        self.add_btn.setObjectName("actionButton")
        self.add_btn.clicked.connect(self._add_task)
        
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.priority_combo)
        input_layout.addWidget(self.add_btn)
        layout.addWidget(input_frame)
        
        self.task_list = QListWidget()
        self.task_list.setSpacing(10)
        layout.addWidget(self.task_list)
        
        self.stack.addWidget(page)

    def _setup_monitor_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        grid = QHBoxLayout()
        self.cpu_chart = LiveMonitorChart(title="CPU PERFORMANCE (%)", color="#7AA2F7")
        self.ram_chart = LiveMonitorChart(title="MEMORY ALLOCATION (%)", color="#BB9AF7")
        grid.addWidget(self.cpu_chart)
        grid.addWidget(self.ram_chart)
        layout.addLayout(grid)
        
        net_grid = QHBoxLayout()
        self.net_up_chart = LiveMonitorChart(title="UPLINK TRAFFIC (KB/s)", color="#F7768E")
        self.net_down_chart = LiveMonitorChart(title="DOWNLINK TRAFFIC (KB/s)", color="#9ECE6A")
        net_grid.addWidget(self.net_up_chart)
        net_grid.addWidget(self.net_down_chart)
        layout.addLayout(net_grid)
        
        self.metrics_label = QLabel("Initializing metrics...")
        self.metrics_label.setStyleSheet("font-family: 'Consolas'; font-size: 11px; color: #565F89;")
        layout.addWidget(self.metrics_label)
        
        self.stack.addWidget(page)

    def _setup_process_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        table_frame = QFrame()
        table_frame.setObjectName("glassCard")
        table_layout = QVBoxLayout(table_frame)
        self.proc_table = ProcessTable()
        table_layout.addWidget(self.proc_table)
        layout.addWidget(table_frame)
        
        self.stack.addWidget(page)

    def _apply_shadow(self):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(25)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.main_container.setGraphicsEffect(self.shadow)

    def _switch_page(self, index):
        # Premium Fade-in effect
        self.fade_anim = QPropertyAnimation(self.stack, b"windowOpacity")
        self.fade_anim.setDuration(300)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self.stack.setCurrentIndex(index)
        self.fade_anim.start()
        
        for i, btn in enumerate(self.nav_btns):
            btn.setProperty("active", i == index)
            btn.setStyle(btn.style())

    def _setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        tray_menu = QMenu()
        show_action = QAction("Restore Control", self)
        show_action.triggered.connect(self.showNormal)
        quit_action = QAction("System Shutdown", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def _toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self._apply_style()
        for chart in [self.cpu_chart, self.ram_chart, self.net_up_chart, self.net_down_chart]:
            chart.set_theme(self.dark_mode)
        # Update tasks
        for i in range(self.task_list.count()):
            widget = self.task_list.itemWidget(self.task_list.item(i))
            if widget: widget.update_state(widget.checkbox.isChecked(), self.dark_mode)

    def _apply_style(self):
        self.setStyleSheet(StyleManager.get_style(self.dark_mode))

    def _add_task(self):
        title = self.task_input.text().strip()
        if not title: return
        task = {"id": str(uuid.uuid4()), "title": title, "priority": self.priority_combo.currentText(), "completed": False}
        self.data_manager.add_task(task)
        self._add_task_widget(task)
        self.task_input.clear()

    def _add_task_widget(self, task):
        item = QListWidgetItem(self.task_list)
        widget = TaskItemWidget(task['id'], task['title'], task['priority'], task['completed'], self.dark_mode)
        widget.deleted.connect(self._delete_task)
        widget.toggled.connect(self._toggle_task_status)
        widget.edited.connect(self._edit_task)
        item.setSizeHint(widget.sizeHint())
        self.task_list.addItem(item)
        self.task_list.setItemWidget(item, widget)

    def _load_tasks_into_list(self):
        self.task_list.clear()
        for task in self.data_manager.load_tasks():
            self._add_task_widget(task)

    def _delete_task(self, task_id):
        self.data_manager.delete_task(task_id)
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            widget = self.task_list.itemWidget(item)
            if widget and widget.task_id == task_id:
                self.task_list.takeItem(i)
                break

    def _toggle_task_status(self, task_id, completed):
        self.data_manager.update_task({"id": task_id, "completed": completed})
        for i in range(self.task_list.count()):
            widget = self.task_list.itemWidget(self.task_list.item(i))
            if widget and widget.task_id == task_id:
                widget.update_state(completed, self.dark_mode)
                break

    def _edit_task(self, task_id, new_title):
        self.data_manager.update_task({"id": task_id, "title": new_title})
        for i in range(self.task_list.count()):
            widget = self.task_list.itemWidget(self.task_list.item(i))
            if widget and widget.task_id == task_id:
                widget.title_label.setText(new_title)
                break

    def _update_all(self):
        self._update_system_metrics()
        if self.stack.currentIndex() == 2:
            self.proc_update_counter += 1
            if self.proc_update_counter >= 3:
                self.proc_table.update_processes(self.system_monitor.get_processes())
                self.proc_update_counter = 0

    def _update_system_metrics(self):
        metrics = self.system_monitor.get_all_metrics()
        self.cpu_chart.update_data(metrics['cpu'])
        self.ram_chart.update_data(metrics['memory']['percent'])
        self.net_up_chart.update_data(metrics['network']['sent'], max_val=200)
        self.net_down_chart.update_data(metrics['network']['recv'], max_val=500)
        self.metrics_label.setText(f"CPU CORE: {metrics['cpu']}%  |  MEM USED: {metrics['memory']['percent']}%  |  NET UP: {metrics['network']['sent']}KB/s")

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()
