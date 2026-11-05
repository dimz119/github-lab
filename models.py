from dataclasses import dataclass, field


@dataclass
class Seat:
    seat_id: str
    held_by: str | None = None

    @property
    def is_available(self) -> bool:
        return self.held_by is None


@dataclass
class Event:
    name: str
    seats: dict[str, Seat] = field(default_factory=dict)

    @classmethod
    def with_seats(cls, name: str, seat_ids: list[str]) -> "Event":
        return cls(name=name, seats={sid: Seat(sid) for sid in seat_ids})
