from setuptools import setup, find_packages

setup(
  name="seekr",
  version="0.1",
  packages=find_packages(),
  install_requires=[
    "typer>=0.9.0",               # CLI
    "python-dotenv>=1.0.0",       # Для .env
    "transformers>=4.35.0",       # Модель и токенизатор
    "torch>=2.0.0",               # Бэкенд для модели
    "accelerate>=0.24.0",         # Для device_map и ускорения
  ],
  entry_points={
    "console_scripts": [
      "seekr=seekr.main:app",
    ],
  },
)
