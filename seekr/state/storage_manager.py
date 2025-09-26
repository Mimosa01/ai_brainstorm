import os
import json
from dotenv import load_dotenv
from typing import Dict, Any, Optional
from pathlib import Path


load_dotenv()
STORAGE_DIR = os.getenv("STORAGE_DIR", "~/Проекты/Seekr/storage")
STORAGE_TREES_DIR = os.getenv("STORAGE_TREES_DIR", "~/Проекты/Seekr/storage/trees")


class StorageManager:
  def __init__(self, base_dir: str = STORAGE_DIR, trees_dir: str = STORAGE_TREES_DIR):
    self.base_dir = os.path.expanduser(base_dir)
    self.trees_dir = os.path.expanduser(trees_dir)

    self.system_file = os.path.join(self.base_dir, "system.json")

    os.makedirs(self.base_dir, exist_ok=True)
    os.makedirs(self.trees_dir, exist_ok=True)

    if not os.path.exists(self.system_file):
      self.save_system({
        "current_tree": None,
        "role": "генератор идей",
        "category": "creative",
        "trees": {}
      })

  def save_system(self, data: Dict[str, Any]) -> None:
    with open(self.system_file, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2, ensure_ascii=False)

  def load_system(self) -> Dict[str, Any]:
    if not os.path.exists(self.system_file):
      return {}
    with open(self.system_file, "r", encoding="utf-8") as f:
      return json.load(f)

  def set_role(self, role: str) -> None:
    data = self.load_system()
    data["role"] = role
    self.save_system(data)

  def get_role(self) -> str:
    return self.load_system().get("role", "генератор идей")

  def set_category(self, category: str) -> None:
    data = self.load_system()
    data["category"] = category
    self.save_system(data)

  def get_category(self) -> str:
    return self.load_system().get("category", "creative")

  def set_current_tree(self, tree_id: Optional[str]) -> None:
    data = self.load_system()
    data["current_tree"] = tree_id
    self.save_system(data)

  def get_current_tree(self) -> Optional[str]:
    return self.load_system().get("current_tree")

  def save_tree(self, tree_id: str, tree_data: Dict[str, Any]) -> None:
    """Сохраняет конкретное дерево и обновляет системный список"""
    path = os.path.join(self.trees_dir, f"{tree_id}.json")
    with open(path, "w", encoding="utf-8") as f:
      json.dump(tree_data, f, indent=2, ensure_ascii=False)

    system = self.load_system()
    system["trees"][tree_id] = path
    self.save_system(system)

  def load_tree(self, tree_id: str) -> Dict[str, Any]:
    path = os.path.join(self.trees_dir, f"{tree_id}.json")
    if not os.path.exists(path):
      raise FileNotFoundError(f"Tree file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
      return json.load(f)

  def list_trees(self) -> Dict[str, str]:
    """Возвращает словарь {tree_id: path}"""
    return self.load_system().get("trees", {})
  
  def delete_tree(self, tree_id) -> None:
    path = os.path.join(self.trees_dir, f"{tree_id}.json")
    if not os.path.exists(path):
      raise FileNotFoundError(f"Tree file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
      os.remove(path)


storage = StorageManager()
