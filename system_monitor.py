import psutil
import datetime
from typing import Dict, Any

class SystemMonitor:
    """
    Handles retrieving real-time system resource metrics.
    """
    @staticmethod
    def get_cpu_usage() -> float:
        """Returns the current CPU usage as a percentage."""
        try:
            return psutil.cpu_percent(interval=None)
        except Exception:
            return 0.0

    @staticmethod
    def get_memory_info() -> Dict[str, float]:
        """Returns memory usage statistics (total, available, percent)."""
        try:
            mem = psutil.virtual_memory()
            return {
                "total": round(mem.total / (1024**3), 2),  # GB
                "available": round(mem.available / (1024**3), 2),  # GB
                "percent": mem.percent
            }
        except Exception:
            return {"total": 0.0, "available": 0.0, "percent": 0.0}

    @staticmethod
    def get_disk_info() -> Dict[str, float]:
        """Returns disk usage statistics for the root partition."""
        try:
            disk = psutil.disk_usage('/')
            return {
                "total": round(disk.total / (1024**3), 2),  # GB
                "used": round(disk.used / (1024**3), 2),    # GB
                "free": round(disk.free / (1024**3), 2),    # GB
                "percent": disk.percent
            }
        except Exception:
            return {"total": 0.0, "used": 0.0, "free": 0.0, "percent": 0.0}

    def get_all_metrics(self) -> Dict[str, Any]:
        """Combines all system metrics into a single dictionary."""
        return {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "cpu": self.get_cpu_usage(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info()
        }
