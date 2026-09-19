import json
import random
from pathlib import Path


CAREERS_PATH = Path("data/careers.json")

with open(CAREERS_PATH, "r", encoding="utf-8") as file:
    CAREERS = json.load(file)


LIVING_COST = 20_000


def get_job_title(character):
    if not character.job:
        return "Unemployed"

    career = CAREERS.get(character.job)

    if not career:
        return "Unemployed"

    levels = career["levels"]

    if character.job_level >= len(levels):
        return levels[-1]["title"]

    return levels[character.job_level]["title"]


def yearly_money(character):
    # Adults have yearly living expenses.
    if character.age >= 18:
        character.money -= LIVING_COST

    # Unemployed characters don't receive a salary.
    if not character.job:
        return

    career = CAREERS.get(character.job)

    if not career:
        return

    levels = career["levels"]

    # Prevent an invalid job level.
    character.job_level = min(
        character.job_level,
        len(levels) - 1
    )

    # Receive salary.
    character.money += levels[character.job_level]["salary"]

    character.years_in_job += 1

    # Promotion check.
    if (
        character.job_level < len(levels) - 1
        and character.years_in_job >= 3
        and random.random() < 0.30
    ):
        character.job_level += 1
        character.years_in_job = 0
        return f"You were promoted to {get_job_title(character)}!"

    return None