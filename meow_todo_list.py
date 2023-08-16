from pydantic import BaseModel
import time
from cat.mad_hatter.decorators import tool, hook
from cat.log import log



#from .todo_save_load import get_todos, save_todos

import os
import pandas as pd


todo_csv_path = os.path.join(
    os.path.dirname(__file__), "todo.csv"
)


def get_todos():
    if not os.path.exists(todo_csv_path):
        return []
    else:
        df = pd.read_csv(todo_csv_path)
        return df.to_dict(orient="records")

    
def save_todos(todos):
    pd.DataFrame(todos).to_csv(todo_csv_path, index=False)


def stringify_todos(todos):
    if len(todos) == 0:
        return "Your todo is empty."
    
    out = "### Todo list:"
    for t in todos:
        out += "\n - " + t["description"]

    return out


@tool(return_direct=True)
def add_todo(todo, cat):
    """Add item to the todo list. User may say "Remeber to..." or similar. Argument "todo" is a string representing the item."""

    todos = get_todos()
    todos.append({
        "created": time.time(),
        "description": str(todo)
    })

    save_todos(todos)

    return f"Todo list updated with: *{todo}*"


@tool(return_direct=True)
def remove_todo(todo, cat):
    """Remove / delete item from the todo list. "todo" is the item to remove."""

    todos = get_todos()

    # TODO: should we use embeddings?
    prompt = "Given this list of items:"
    for t_index, t in enumerate(todos):
        prompt += f"\n {t_index}. {t['description']}"
    prompt += f"\n\nThe most similar item to `{todo}` is item number... (reply ONLY with the number, no letters or points)"
    
    
    try:
        to_remove = cat.llm(prompt)
        index_to_remove = int(to_remove)

        todos.pop(index_to_remove)
        save_todos(todos)
    except Exception as e:
        log(e, "ERROR")
        return f"Sorry there was an error: {e}. Can you ask in a different way?"
    
    return stringify_todos(todos)


@tool(return_direct=True)
def search_todo(query, cat):
    """Get things in the todo list. "query" is a string used to filter the list."""
    
    todos = get_todos()
    return stringify_todos(todos)

