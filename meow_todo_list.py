from pydantic import BaseModel
from ast import literal_eval
import time

from cat.mad_hatter.decorators import tool, hook
from cat.log import log

from .todo import get_todos, save_todos, stringify_todos


@tool(return_direct=True)
def add_todo(todo, cat):
    """Add item or multiple items to the todo list. User may say "Remeber to..." or similar. Input is an array of items."""

    try:
        todo = literal_eval(todo)
    except Exception as e:
        log(e, "ERROR")
        return f"Sorry there was an error: {e}. Can you ask in a different way?"
    todos = get_todos()
    for elem in todo:
        todos.append({
            "created": time.time(),
            "description": str(elem)
        })

    save_todos(todos)

    return f"Todo list updated with: *{', '.join(todo)}*"


@tool(return_direct=True)
def remove_todo(todo, cat):
    """Remove / delete item or multiple items from the todo list. Input is the array of items to remove."""
    todos = get_todos()

    # TODO: should we use embeddings?
    prompt = "Given this list of items:"
    for t_index, t in enumerate(todos):
        prompt += f"\n {t_index}. {t['description']}"
    prompt += f"\n\nThe most similar items to `{todo}` are items number... (reply ONLY with an array with the number or numbers, no letters or points)"
    try:
        to_remove = cat.llm(prompt)
        index_to_remove = literal_eval(to_remove)
        todos = [el for idx, el in enumerate(todos) if idx not in index_to_remove]
        save_todos(todos)
    except Exception as e:
        log(e, "ERROR")
        return f"Sorry there was an error: {e}. Can you ask in a different way?"
    
    return stringify_todos(todos)


@tool(return_direct=True)
def list_todo(query, cat):
    """List what is in the todo list. Input is a string used to filter the list."""
    
    todos = get_todos()
    return stringify_todos(todos)

