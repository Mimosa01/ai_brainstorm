from typing import List
from seekr.constants import PROMPTS
from seekr.exceptions import PromptError


def get_prompt(category: str, role: str = "ассистент", max_words: int = 10) -> str:
  """
  Возвращает промпт с подставленной ролью для выбранной категории.
  """
  try:
    if category not in PROMPTS:
      raise PromptError(f"Неизвестная категория промпта: {category}")

    template = PROMPTS[category]

    try:
      return template.format(role=role, max_words=max_words)
    except Exception as e:
      raise PromptError(f"Ошибка при форматировании шаблона для категории '{category}': {e}") from e

  except KeyError as e:
    raise PromptError(f"Категория '{category}' отсутствует в PROMPTS.") from e


def get_categories_prompts() -> List[str]:
  """
  Возвращает список категорий промптов.
  """
  try:
    return list(PROMPTS.keys())
  except Exception as e:
    raise PromptError(f"Не удалось получить список категорий промптов: {e}") from e

