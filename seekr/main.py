from typer import Typer
from seekr.commands import tree_cmd
from seekr.commands import model_cmd


app = Typer(help='Seekr CLI. Автоматизация креатива. Утилита будет строить дерево идей на основе главной темы с заданой глубиной и шириной')

app.add_typer(tree_cmd.app)
app.add_typer(model_cmd.app)

if __name__ == "__main__":
  app()