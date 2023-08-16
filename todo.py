
import os
import pandas as pd


todo_csv_path = os.path.join(
    os.path.dirname(__file__), "todo.csv"
)


def stringify_todos(todos):
    if len(todos) == 0:
        return "Your todo is empty."
    
    out = "### Todo list:"
    for t in todos:
        out += "\n - " + t["description"]

    return out


def get_todos():
    if not os.path.exists(todo_csv_path):
        return []
    else:
        df = pd.read_csv(todo_csv_path)
        return df.to_dict(orient="records")

    
def save_todos(todos):
    pd.DataFrame(todos).to_csv(todo_csv_path, index=False)