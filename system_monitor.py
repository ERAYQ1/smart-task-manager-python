import psutil
import datetime
from typing import Dict, Any

class SystemMonitor:
    @staticmethod
    def get_cpu_usage() -> float:
        try:
            return psutil.cpu_percent(interval=None)
        except Exception:
            return 0.0

    @staticmethod
    def get_memory_info() -> Dict[str, float]:
        try:
            mem = psutil.virtual_memory()
            return {
                "total": round(mem.total / (1024**3), 2),
                "available": round(mem.available / (1024**3), 2),
                "percent": mem.percent
            }
        except Exception:
            return {"total": 0.0, "available": 0.0, "percent": 0.0}

    @staticmethod
    def get_disk_info() -> Dict[str, float]:
        try:
            disk = psutil.disk_usage('/')
            return {
                "total": round(disk.total / (1024**3), 2),
                "used": round(disk.used / (1024**3), 2),
                "free": round(disk.free / (1024**3), 2),
                "percent": disk.percent
            }
        except Exception:
            return {"total": 0.0, "used": 0.0, "free": 0.0, "percent": 0.0}

    def get_all_metrics(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "cpu": self.get_cpu_usage(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info()
        }
