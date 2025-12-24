import json
import os
from typing import List, Dict, Any

class DataManager:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def load_tasks(self) -> List[Dict[str, Any]]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_tasks(self, tasks: List[Dict[str, Any]]):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def add_task(self, task: Dict[str, Any]):
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)

    def delete_task(self, task_id: Any):
        tasks = self.load_tasks()
        tasks = [t for t in tasks if t.get('id') != task_id]
        self.save_tasks(tasks)

    def update_task(self, updated_task: Dict[str, Any]):
        tasks = self.load_tasks()
        for i, task in enumerate(tasks):
            if task.get('id') == updated_task.get('id'):
                tasks[i] = updated_task
                break
        self.save_tasks(tasks)
