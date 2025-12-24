import json
import os
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataManager:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            try:
                with open(self.filename, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
            except Exception as e:
                logging.error(f"Could not create data file: {e}")

    def load_tasks(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.warning(f"Error loading tasks, returning empty list: {e}")
            return []

    def save_tasks(self, tasks: List[Dict[str, Any]]):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"Error saving tasks: {e}")

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
                # Merge the dictionaries to preserve existing fields
                tasks[i].update(updated_task)
                break
        self.save_tasks(tasks)
