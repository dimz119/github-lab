import pytest

from models import Event
from seat_service import (
    SeatAlreadyHeld,
    SeatNotFound,
    available_seats,
    hold,
    release,
)


@pytest.fixture
def event():
    return Event.with_seats("concert", ["A1", "A2", "A3"])


def test_hold_marks_seat_as_taken(event):
    hold(event, "A1", "alice")
    assert event.seats["A1"].held_by == "alice"
    assert available_seats(event) == ["A2", "A3"]


def test_cannot_hold_same_seat_twice(event):
    hold(event, "A1", "alice")
    with pytest.raises(SeatAlreadyHeld):
        hold(event, "A1", "bob")


def test_hold_unknown_seat(event):
    with pytest.raises(SeatNotFound):
        hold(event, "Z9", "alice")


def test_release_frees_seat(event):
    hold(event, "A1", "alice")
    release(event, "A1", "alice")
    assert event.seats["A1"].is_available


def test_only_holder_can_release(event):
    hold(event, "A1", "alice")
    with pytest.raises(PermissionError):
        release(event, "A1", "bob")
