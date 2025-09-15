import os
from typing import List
from collections import deque
from typer import echo
from transformers import AutoTokenizer, AutoModelForCausalLM
from functools import lru_cache

from seekr.utils.get_prompts import get_prompt
from seekr.state.node import Node
from seekr.state.storage_manager import StorageManager, storage
from seekr.exceptions import GenerationError


MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-1.5B-Instruct")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 50))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.8))
TOP_P = float(os.getenv("TOP_P", 0.9))
MAX_WORDS = int(os.getenv("MAX_WORDS", 10))
DEFAULT_ROLE_MODEL = os.getenv("DEFAULT_ROLE_MODEL", "генератор идей")
DEFAULT_CATEGORY_TEMPLATE = os.getenv("DEFAULT_CATEGORY_TEMPLATE", "creative")

MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-1.5B-Instruct")

@lru_cache(maxsize=1)
def get_model_and_tokenizer():
  """
  Возвращает кортеж (tokenizer, model).
  Загружается только один раз за процесс.
  """
  tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
  model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map={"": "cpu"},
    trust_remote_code=True
  )
  return tokenizer, model


class IdeaGenerator:
  def __init__(self, storage: StorageManager) -> None:
    self.storage = storage
    self.__role = DEFAULT_ROLE_MODEL
    self.__category = DEFAULT_CATEGORY_TEMPLATE

  @property
  def role(self) -> str:
    return self.storage.get_role() or DEFAULT_ROLE_MODEL

  @role.setter
  def role(self, role: str | None = None) -> None:
    if role:
      self.storage.set_role(role)
    else:
      self.storage.set_role(DEFAULT_ROLE_MODEL)

  @property
  def category(self) -> str:
    return self.storage.get_category() or DEFAULT_CATEGORY_TEMPLATE

  @category.setter
  def category(self, category: str | None = None) -> None:
    if category:
      self.storage.set_category(category)
    else:
      self.storage.set_category(DEFAULT_CATEGORY_TEMPLATE)

  def generate(self, text: str, n_variants: int) -> List[str]:
    """
    Генерация идей напрямую через модель (без сервера).
    """
    tokenizer, model = get_model_and_tokenizer()

    ideas = []
    for i in range(n_variants):
      try:
        messages = [
          {"role": "system", "content": get_prompt(self.__category, role=self.__role, max_words=MAX_WORDS)},
          {"role": "user", "content": f"Исходная идея: {text}"},
        ]

        prompt_text = tokenizer.apply_chat_template(
          messages, tokenize=False, add_generation_prompt=True
        )

        inputs = tokenizer([prompt_text], return_tensors="pt").to(model.device)
        outputs = model.generate(
          **inputs,
          max_new_tokens=MAX_TOKENS,
          do_sample=True,
          temperature=TEMPERATURE,
          top_p=TOP_P
        )

        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(inputs.input_ids, outputs)
        ]
        idea = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        ideas.append(idea)

      except Exception as e:
        raise GenerationError(f"Ошибка при генерации идеи №{i+1}: {e}") from e

    if not ideas:
      raise GenerationError("Генерация завершилась без результатов.")

    return ideas

  def expand_tree(self, node: Node, depth: int, breadth: int):
    """
    Обход в ширину: строит дерево до depth уровней.
    breadth - сколько детей создавать у каждого узла.
    """
    if depth <= 0:
      echo("Ошибка: глубина дерева должна быть больше 0")
      return
    if breadth <= 0:
      echo("Ошибка: ширина дерева должна быть больше 0")
      return

    queue = deque([(node, 1)])

    while queue:
      current_node, level = queue.popleft()

      if level > depth:
        continue

      try:
        children = self.generate(current_node.text, breadth)
      except MemoryError:
        echo("Недостаточно памяти для генерации идей. Попробуйте уменьшить ширину или глубину.")
        return
      except GenerationError as e:
        echo(f"Ошибка генерации идей: {e}")
        return

      for child_text in children:
        try:
          child_node = current_node.add_child(child_text)
          queue.append((child_node, level + 1))
        except Exception as e:
          echo(f"Не удалось добавить узел '{child_text}': {e}")


generator = IdeaGenerator(storage=storage)
