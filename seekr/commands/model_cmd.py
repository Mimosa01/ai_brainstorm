from typer import Typer, Argument, Option, echo
from seekr.ai.idea_generate import generator
from seekr.utils.get_prompts import get_categories_prompts


app = Typer(help='Работа с ролью модели')

VALID_CATEGORIES = get_categories_prompts()


@app.command()
def role(
    role_text: str = Argument(None, help="Новая роль модели"),
    reset: bool = Option(False, "--reset", "-r", help="Сбросить роль к дефолтной")
):
    """
    Управление ролью модели.
    
    - Без аргумента: выводит текущую роль.
    - С аргументом: задаёт новую роль.
    - С флагом --reset: сбрасывает роль к дефолтной.
    """
    if reset:
        generator.role = None
        echo(f"Роль сброшена к дефолтной: {generator.role}")
        return

    if role_text:
        generator.role = role_text
        echo(f"Роль успешно изменена на: {role_text}")
    else:
        echo(f"Текущая роль модели: {generator.role}")


@app.command()
def category(
  new_category: str = Argument(None, help=f"Новая категория. Доступные: {', '.join(VALID_CATEGORIES)}"),
  reset: bool = Option(False, "--reset", "-r", help="Сбросить категорию к дефолтной"),
  show_list: bool = Option(False, "--list", "-l", help="Показать все доступные категории")
):
  """
  Управление категорией генерации идей.
  
  - Без аргумента: выводит текущую категорию.
  - С аргументом: задаёт новую категорию из списка.
  - С флагом --reset: сбрасывает категорию к дефолтной.
  - С флагом --list: выводит список всех доступных категорий.
  """

  if show_list:
    echo("Доступные категории:")
    for cat in VALID_CATEGORIES:
      echo(f" - {cat}")
    return
  
  if reset:
    generator.category = None
    echo(f"Категория сброшена к дефолтной: {generator.category}")
    return

  if new_category:
    if new_category not in VALID_CATEGORIES:
      echo(f"Ошибка: '{new_category}' недопустимая категория. Доступные: {', '.join(VALID_CATEGORIES)}")
      return
    generator.category = new_category
    echo(f"Категория успешно изменена на: {new_category}")
  else:
    echo(f"Текущая категория модели: {generator.category}")
