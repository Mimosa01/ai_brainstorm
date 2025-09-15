from typing import Optional
from seekr.state.node import Node
from seekr.utils.id_gen import id_generate


class Tree:
  def __init__(self, root_text: str, tree_id: str | None = None):
    self.root = Node(root_text)
    self.__id = tree_id or id_generate()

  @property
  def id (self) -> str:
    return self.__id

  def find(self, node_id: str) -> Optional[Node]:
    return self._find_recursive(self.root, node_id)

  def _find_recursive(self, node: Node, node_id: str) -> Optional[Node]:
    if node.id == node_id:
      return node
    for child in node.children:
      result = self._find_recursive(child, node_id)
      if result:
        return result
    return None

  def add_node(self, parent_id: str, text: str) -> Optional[Node]:
    parent = self.find(parent_id)
    if parent:
      return parent.add_child(text)
    return None
  
  def to_dict(self) -> dict:
    return {
      "id": self.__id,
      "root": self.root.to_dict()
    }
  
  @classmethod
  def from_dict(cls, data: dict) -> "Tree":
    tree = cls(data["root"]["text"], tree_id=data["id"])
    tree.root = Node.from_dict(data["root"])
    return tree