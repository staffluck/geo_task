from dataclasses import dataclass


@dataclass
class User:
    email: str
    password: str
    first_name: str | None
    last_name: str | None
