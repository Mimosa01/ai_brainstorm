import json
from typing import Optional
from seekr.state.tree import Tree
from seekr.state.storage_manager import storage, StorageManager


class TreeManager:
  def __init__(self, storage: StorageManager):
    self.storage = storage
    self.trees: dict[str, Tree] = {}
    self.current_tree: Optional[str] = None
    self.load_state()

  def create_tree(self, root_text: str) -> Tree:
    tree = Tree(root_text)
    self.trees[tree.id] = tree
    self.current_tree = tree.id

    self.storage.save_tree(tree.id, tree.to_dict())
    self.storage.set_current_tree(tree.id)

    return tree

  def switch_tree(self, tree_id: str) -> bool:
    if tree_id in self.trees:
      self.current_tree = tree_id
      self.storage.set_current_tree(tree_id)
      return True
    return False

  def list_trees(self) -> list[dict]:
    return [{"id": t.id, "name": t.root.text} for t in self.trees.values()]

  def get_current_tree(self) -> Optional[Tree]:
    if self.current_tree:
      return self.trees.get(self.current_tree)
    return None
  
  def save_state(self):
    """Сохраняем все деревья через StorageManager"""
    for tree_id, tree in self.trees.items():
      self.storage.save_tree(tree_id, tree.to_dict())
    if self.current_tree:
      self.storage.set_current_tree(self.current_tree)

  def load_state(self):
    """Восстанавливаем состояние из StorageManager"""
    self.trees = {}
    trees_meta = self.storage.list_trees()
    for tree_id in trees_meta.keys():
      tree_data = self.storage.load_tree(tree_id)
      self.trees[tree_id] = Tree.from_dict(tree_data)
    self.current_tree = self.storage.get_current_tree()

  def delete_tree(self, tree_id: str) -> None:
    storage.delete_tree(tree_id)
  

tree_manager = TreeManager(storage=storage)