from typer import Typer, Option, echo, Exit
from typing import Optional
from seekr.state.tree_manager import tree_manager
from seekr.utils import print_tree_human, print_forest
from seekr.ai.idea_generate import generator


app = Typer(help="Работа с деревом идей")

from typing import Optional
from typer import Option, echo, Argument

@app.command()
def idea(
  text: Optional[str] = Argument(None, help="Текст новой идеи (требуется только для нового дерева)"),
  parent: Optional[str] = Option(None, "--parent", help="ID родительского узла для создания дочернего узла"),
  depth: int = Option(1, "-d", "--depth", help="Глубина создаваемого дерева"),
  breadth: int = Option(3, "-b", "--breadth", help="Ширина создаваемого дерева"),
):
  """Создание новой идеи (новое дерево или дочерний узел)."""

  # --- Если указан родитель ---
  if parent:
    current_tree = tree_manager.get_current_tree()
    if not current_tree:
      echo("Нет активного дерева. Сначала создайте дерево.")
      return

    parent_node = current_tree.find(parent)
    if not parent_node:
      echo(f"Родитель с id={parent} не найден")
      return

    # либо расширяем существующий узел, либо создаём новый
    target_node = (
      current_tree.add_node(parent_id=parent_node.id, text=f"{parent_node.text} {text}")
      if text else parent_node
    )

    if target_node:
      echo(f"Добавляем дочерние идеи к узлу: {target_node.text} (id={target_node.id})")
      generator.expand_tree(target_node, depth, breadth)
    tree_manager.save_state()

  # --- Если родитель не указан → создаём новое дерево ---
  else:
    if not text:
      echo("Для создания нового дерева необходимо указать текст идеи.")
      return

    tree = tree_manager.create_tree(text)
    echo(f"Создано новое дерево: {tree.id}")
    echo(f"Корневой узел: {tree.root.text} (id={tree.root.id})")

    generator.expand_tree(tree.root, depth, breadth)
    tree_manager.save_state()

  # --- Общая часть (для обоих сценариев) ---
  current_tree = tree_manager.get_current_tree()
  if current_tree:
    print_tree_human(current_tree.root)

  echo(f"Параметры генерации: глубина={depth}, ширина={breadth}")


@app.command()
def delete(id: str = Argument(None, help="Удалить дерево с выбранным id")):
  try:
    tree_manager.delete_tree(id)
    echo(f'Дерево [{id}] - Успешно удалено')
  except FileNotFoundError:
    echo('Ошибка обработки файла')

@app.command()
def show(short: bool = Option(False, "--short", "-s", is_flag=True, help="Показывать только id дерева")):
  """Отобразить текущее дерево в человекочитаемом виде или только id текущего дерева"""

  current_tree = tree_manager.get_current_tree()
  if not current_tree:
    echo("Нет активного дерева. Сначала создайте дерево.")
    return
  
  if short:
    echo(f"ID Tree {current_tree.id}")
  else:
    echo(f"Дерево идей (ID: {current_tree.id}):")
    print_tree_human(current_tree.root)


@app.command()
def switch(
  id: str = Option(..., "--id", "-i", help="ID дерева для переключения")
):
  """Переключить активное дерево по ID"""
  if tree_manager.switch_tree(id):
    echo(f"Переключение на дерево с ID: {id}")
  else:
    echo(f"Дерева с таким ID не существует")
    raise Exit(code=1)


@app.command()
def list ():
  """Показать список деревьев"""

  echo(f'Показываю список деревьев с именами и идентификаторами')
  print_forest(tree_manager.list_trees())