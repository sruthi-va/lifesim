from game.character import Character
from game.systems.health import yearly_health, check_death


name = input("What is your name? ")

c = Character(name)

while c.alive:
    input(f"[Age {c.age}] Press Enter to age up... ")

    c.age += 1

    yearly_health(c)
    check_death(c)

    print(
        f"Age {c.age} | "
        f"HP {c.health} | "
        f"Happy {c.happiness} | "
        f"Smarts {c.smarts} | "
        f"Looks {c.looks} | "
        f"${c.money}"
    )

print()
print(f"{c.name} died at age {c.age}.")