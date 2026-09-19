import tkinter as tk
from tkinter import simpledialog, messagebox

from game.character import Character
from game.engine import Engine
from game.data_loader import load_events
from ui.app import App


def main():
    root = tk.Tk()

    name = simpledialog.askstring(
        "Life Sim",
        "What is your name?",
        parent=root
    )

    if not name:
        root.destroy()
        return

    character = Character(name)
    events = load_events()
    engine = Engine(character, events)

    App(root, engine)

    root.mainloop()


if __name__ == "__main__":
    main()