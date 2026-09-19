import random

from game.systems.health import yearly_health, check_death


STATS = ("health", "happiness", "smarts", "looks")


def eligible(event, character):
    conditions = event.get("conditions", {})

    min_age = conditions.get("min_age", 0)
    max_age = conditions.get("max_age", 200)

    if not (min_age <= character.age <= max_age):
        return False

    required_flags = set(conditions.get("requires_flags", []))

    if not required_flags <= character.flags:
        return False

    forbidden_flags = set(conditions.get("forbids_flags", []))

    if forbidden_flags & character.flags:
        return False

    min_money = conditions.get("min_money", -10**9)

    if character.money < min_money:
        return False

    last_seen = character.seen.get(event["id"])

    if last_seen is not None:
        if event.get("once"):
            return False

        cooldown = event.get("cooldown", 0)

        if character.age - last_seen < cooldown:
            return False

    return True


def pick_event(events, character, exclude=None):
    if exclude is None:
        exclude = []

    pool = [
        event
        for event in events
        if eligible(event, character) and event not in exclude
    ]

    if not pool:
        return None

    weights = [event.get("weight", 1) for event in pool]

    return random.choices(pool, weights=weights, k=1)[0]


def apply_effects(character, effects):
    for stat in STATS:
        if stat in effects:
            new_value = getattr(character, stat) + effects[stat]

            new_value = max(0, min(100, new_value))

            setattr(character, stat, new_value)

    character.money += effects.get("money", 0)


def resolve(character, event, choice):
    chosen_result = choice

    if "outcomes" in choice:
        roll = random.random()
        total = 0

        chosen_result = choice["outcomes"][-1]

        for outcome in choice["outcomes"]:
            total += outcome["chance"]

            if roll <= total:
                chosen_result = outcome
                break

    apply_effects(
        character,
        chosen_result.get("effects", {})
    )

    character.flags |= set(
        chosen_result.get("set_flags", [])
    )

    character.flags -= set(
        chosen_result.get("clear_flags", [])
    )

    character.seen[event["id"]] = character.age

    return chosen_result.get("result", "")


class Engine:

    def __init__(self, character, events):
        self.c = character
        self.events = events

    def age_up(self):
        self.c.age += 1

        yearly_health(self.c)

        picked_events = []

        number_of_events = random.choice([1, 1, 2])

        for _ in range(number_of_events):
            event = pick_event(
                self.events,
                self.c,
                exclude=picked_events
            )

            if event:
                picked_events.append(event)

        return picked_events

    def resolve(self, event, choice):
        return resolve(self.c, event, choice)

    def check_death(self):
        return check_death(self.c)