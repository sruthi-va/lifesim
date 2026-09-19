from dataclasses import dataclass, field


@dataclass
class Character:
    name: str

    age: int = 0
    alive: bool = True

    health: int = 80
    happiness: int = 70
    smarts: int = 50
    looks: int = 50

    money: int = 0

    job: str | None = None
    job_level: int = 0
    years_in_job: int = 0

    flags: set = field(default_factory=set)
    seen: dict = field(default_factory=dict)
    people: list = field(default_factory=list)
    log: list = field(default_factory=list)