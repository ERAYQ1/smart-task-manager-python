# Smart Task Manager & System Monitor

A modern, offline, and desktop application for task management integrated with real-time system resource monitoring.

## Features
- **Task Management**: Add, delete, and toggle tasks with priority levels.
- **System Monitoring**: Live CPU, RAM, and Disk usage tracking.
- **Dynamic Charts**: Real-time data visualization using Matplotlib.
- **Dark/Light Themes**: Modern UI with theme-switching capability.
- **Data Persistence**: Automatic saving and loading of tasks via JSON.

## Project Structure
- `main.py`: Entry point for the application.
- `gui.py`: Main window and UI assembly.
- `data_manager.py`: Handles task storage and data logic.
- `system_monitor.py`: Retrieves real-time hardware metrics.
- `components.py`: Custom UI widgets and interactive charts.
- `styles.py`: Centralized management of UI themes (QSS).

## Requirements
- Python 3.8+
- PySide6
- psutil
- matplotlib

## Installation
```bash
pip install PySide6 psutil matplotlib
```

## Usage
Run the application using:
```bash
python main.py
```
