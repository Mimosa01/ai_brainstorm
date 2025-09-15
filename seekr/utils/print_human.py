from typer import echo, style
from seekr.constants import LEVEL_COLORS

def print_tree_human(node, prefix="", is_last=True, level=0):
  """
  Выводит дерево идей в человекочитаемом виде
  """
  try:
    if not node:
      raise ValueError("Передан пустой узел дерева")

    connector = "└─" if is_last else "├─"
    color = LEVEL_COLORS[level % len(LEVEL_COLORS)]
    node_text = style(f"{node.text} (id={node.id})", fg=color)
    echo(f"{prefix}{connector} {node_text}")

    new_prefix = prefix + ("   " if is_last else "│  ")

    for i, child in enumerate(node.children):
      print_tree_human(child, new_prefix, i == len(node.children) - 1, level + 1)

  except Exception as e:
    echo(style(f"[Ошибка при выводе дерева] {e}", fg="red", bold=True))


def print_forest(trees: list):
  """
  Выводит список деревьев (список словарей с ключами 'id' и 'name') в человекочитаемом виде.
  """
  try:
    if not trees:
      echo(style("Список деревьев пуст.", fg="yellow", bold=True))
      return

    echo(style("Список деревьев:", fg="cyan", bold=True))
    for i, tree in enumerate(trees, start=1):
      if not isinstance(tree, dict):
        raise TypeError(f"Неверный формат дерева: {tree}")

      tree_id = tree.get("id", "<no id>")
      tree_name = tree.get("name", "<no name>")
      echo(style(f"{i}. {tree_name} (ID: {tree_id})", fg="green"))

  except Exception as e:
    echo(style(f"[Ошибка при выводе списка деревьев] {e}", fg="red", bold=True))
