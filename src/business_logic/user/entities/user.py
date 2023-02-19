from __future__ import annotations

from dataclasses import dataclass


@dataclass
class User:
    id: int
    email: str
    password: str
    first_name: str
    last_name: str | None

    @classmethod
    def create(
        cls, email: str, password: str, first_name: str | None, last_name: str | None
    ) -> User:
        return cls(
            id=None,  # type: ignore
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
