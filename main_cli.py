from game.character import Character
from game.engine import Engine
from game.data_loader import load_events


def display_event(event):
    print()
    print(event["text"])
    print()

    for index, choice in enumerate(event["choices"], start=1):
        print(f"{index}. {choice['label']}")


def choose_option(event):
    choices = event["choices"]

    while True:
        answer = input("\nChoose: ")

        try:
            choice_number = int(answer)
        except ValueError:
            print("Please enter a number.")
            continue

        if 1 <= choice_number <= len(choices):
            return choices[choice_number - 1]

        print("Please choose one of the listed options.")


name = input("What is your name? ")

character = Character(name)

events = load_events()

engine = Engine(character, events)

print()
print(f"Welcome to your life, {character.name}!")


while character.alive:
    input(
        f"\n[Age {character.age}] "
        "Press Enter to age up..."
    )

    events_this_year = engine.age_up()

    print()
    print("=" * 60)
    print(f"AGE {character.age}")
    print("=" * 60)

    if events_this_year:
        for event in events_this_year:
            display_event(event)
            choice = choose_option(event)
            result = engine.resolve(event, choice)
            print()
            print("->", result)

    engine.check_death()

    print()
    print(
        f"Health: {character.health} | "
        f"Happiness: {character.happiness} | "
        f"Smarts: {character.smarts} | "
        f"Looks: {character.looks} | "
        f"Money: ${character.money}"
    )


print()
print("=" * 60)
print(f"{character.name} died at age {character.age}.")
print("=" * 60)