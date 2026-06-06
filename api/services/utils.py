from random import randint
from typing import Any, Dict


def generate_unique_id(database: Dict[int, Any], start: int, end: int):
    while True:
        new_id: int = randint(start, end)
        if new_id not in database:
            return new_id
