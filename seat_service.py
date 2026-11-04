from models import Event


class SeatNotFound(Exception):
    pass


class SeatAlreadyHeld(Exception):
    pass


def hold(event: Event, seat_id: str, user_id: str) -> None:
    """좌석을 user_id 앞으로 잡는다. 이미 잡힌 좌석이면 예외."""
    seat = event.seats.get(seat_id)
    if seat is None:
        raise SeatNotFound(seat_id)
    seat.held_by = user_id


def release(event: Event, seat_id: str, user_id: str) -> None:
    """본인이 잡은 좌석만 풀 수 있다."""
    seat = event.seats.get(seat_id)
    if seat is None:
        raise SeatNotFound(seat_id)
    if seat.held_by != user_id:
        raise PermissionError(f"{user_id} does not hold {seat_id}")
    seat.held_by = None


def available_seats(event: Event) -> list[str]:
    return sorted(sid for sid, seat in event.seats.items() if seat.is_available)
