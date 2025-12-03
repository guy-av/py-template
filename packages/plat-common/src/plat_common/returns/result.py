"""Utility helpers for `returns.result`."""

from returns.maybe import Maybe, Nothing, Some
from returns.result import Result, Success


def result_to_maybe[T, E](result: Result[T, E]) -> Maybe[T]:
    """Convert a result to a maybe."""
    match result:
        case Success(value):
            return Some(value)

    return Nothing
