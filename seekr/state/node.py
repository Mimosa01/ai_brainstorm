from typing import List, Optional
from seekr.utils.id_gen import id_generate


class Node:
  def __init__(self, text: str, parent: Optional['Node'] = None, node_id: str | None = None) -> None:
    self.id: str = node_id or id_generate()
    self.text: str = text
    self.parent: Optional[Node] = parent
    self.children: List[Node] = []

  def add_child (self, text) -> 'Node':
    node = Node(text, parent=self)
    self.children.append(node)
    return node

  def to_dict(self) -> dict:
    return {
      "id": self.id,
      "text": self.text,
      "children": [c.to_dict() for c in self.children],
    }

  @classmethod
  def from_dict(cls, data: dict, parent: "Node | None" = None) -> "Node":
    """
    Восстановление узла и его потомков из словаря
    """
    node = cls(data["text"], parent=parent, node_id=data["id"])
    node.id = data["id"]
    for child_data in data.get("children", []):
      child_node = cls.from_dict(child_data, parent=node)
      node.children.append(child_node)
    return node  