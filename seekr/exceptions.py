class SeekrError(Exception):
    """Базовое исключение для всех ошибок приложения."""


class GenerationError(SeekrError):
    """Ошибка во время генерации идей."""


class StorageError(SeekrError):
    """Ошибка при сохранении или загрузке данных."""


class TreeError(SeekrError):
    """Ошибка работы с деревьями."""


class PromptError(SeekrError):
    """Ошибка при работе с промптами."""
