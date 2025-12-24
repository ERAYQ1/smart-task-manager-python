import psutil
import datetime
import time
from typing import Dict, Any, List

class SystemMonitor:
    def __init__(self):
        self.last_net_io = psutil.net_io_counters()
        self.last_time = time.time()

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

    def get_network_speed(self) -> Dict[str, float]:
        try:
            current_net_io = psutil.net_io_counters()
            current_time = time.time()
            elapsed = current_time - self.last_time
            if elapsed <= 0: elapsed = 0.1
            
            sent_speed = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / elapsed / 1024 # KB/s
            recv_speed = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / elapsed / 1024 # KB/s
            
            self.last_net_io = current_net_io
            self.last_time = current_time
            
            return {"sent": round(sent_speed, 2), "recv": round(recv_speed, 2)}
        except Exception:
            return {"sent": 0.0, "recv": 0.0}

    @staticmethod
    def get_processes() -> List[Dict[str, Any]]:
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    pinfo['cpu_percent'] = round(pinfo.get('cpu_percent', 0), 1)
                    pinfo['memory_percent'] = round(pinfo.get('memory_percent', 0), 1)
                    processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:50]
        except Exception:
            return []

    def get_all_metrics(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "cpu": self.get_cpu_usage(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_speed()
        }
