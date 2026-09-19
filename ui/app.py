import tkinter as tk
from tkinter import ttk, scrolledtext


class App:
    def __init__(self, root, engine):
        self.engine = engine
        self.pending = []

        root.title("Life Sim")
        root.geometry("750x600")

        # Stats at the top
        self.stats = ttk.Label(
            root,
            font=("Consolas", 11)
        )
        self.stats.pack(
            anchor="w",
            padx=8,
            pady=6
        )

        # Main game log
        self.log = scrolledtext.ScrolledText(
            root,
            width=80,
            height=22,
            wrap="word",
            state="disabled"
        )
        self.log.pack(
            padx=8,
            fill="both",
            expand=True
        )

        # Event choice buttons
        self.choices = ttk.Frame(root)
        self.choices.pack(
            fill="x",
            padx=8,
            pady=6
        )

        # Age Up button
        self.age_btn = ttk.Button(
            root,
            text="Age Up",
            command=self.age_up
        )
        self.age_btn.pack(pady=6)

        self.refresh()

    def write(self, text):
        self.log.config(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def refresh(self):
        c = self.engine.c

        job = c.job or "unemployed"

        self.stats.config(
            text=(
                f"{c.name}, Age {c.age} ({job})   "
                f"HP {c.health}  "
                f"Happy {c.happiness}  "
                f"Smarts {c.smarts}  "
                f"Looks {c.looks}  "
                f"${c.money:,}"
            )
        )

    def age_up(self):
        self.pending = self.engine.age_up()

        self.write("")
        self.write(f"--- Age {self.engine.c.age} ---")

        for message in self.engine.last_year_messages:
            self.write(message)

        self.next_event()

    def next_event(self):
        # Remove old choice buttons
        for widget in self.choices.winfo_children():
            widget.destroy()

        # No events left this year
        if not self.pending:

            if self.engine.check_death():
                self.write("")
                self.write(
                    f"{self.engine.c.name} died at "
                    f"age {self.engine.c.age}."
                )

                self.age_btn.state(["disabled"])

            else:
                self.age_btn.state(["!disabled"])

            self.refresh()
            return

        # Get the next event
        event = self.pending.pop(0)

        self.write(event["text"])

        # Create a button for each choice
        for choice in event["choices"]:
            ttk.Button(
                self.choices,
                text=choice["label"],
                command=lambda choice=choice, event=event:
                    self.choose(event, choice)
            ).pack(
                fill="x",
                pady=2
            )

        # Can't age while answering an event
        self.age_btn.state(["disabled"])

    def choose(self, event, choice):
        result = self.engine.resolve(event, choice)

        self.write("-> " + result)

        self.refresh()

        self.next_event()