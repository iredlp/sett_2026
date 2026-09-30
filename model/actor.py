
from dataclasses import dataclass, field
from datetime import date

@dataclass
class Actor:
    id: str
    name: str
    height: int
    date_of_birth: date
    known_for_movies: str

    movies: list = field(default_factory=list)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Actor):
            return self.id == other.id
        return False

    def __repr__(self):
        return f"{self.name} ({self.id if self.id is not None else 'N/D'})"