import eel

from data.todo import Todo
todo_app = Todo()


@eel.expose
def delete(task):
    todo_app.delete(task)
