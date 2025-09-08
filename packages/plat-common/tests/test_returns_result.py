"""Tests for the `result_to_maybe` conversion utility."""

from plat_common.returns.result import result_to_maybe
from returns.maybe import Nothing, Some
from returns.result import Failure, Success


def test_result_to_maybe_success() -> None:
    """`result_to_maybe` returns `Some` when given `Success`."""
    answer = 42

    result = Success(answer)
    maybe = result_to_maybe(result)

    assert isinstance(maybe, Some)
    assert maybe.unwrap() == answer


def test_result_to_maybe_failure() -> None:
    """`result_to_maybe` returns `Nothing` when given `Failure`."""
    result = Failure("error")
    maybe = result_to_maybe(result)

    assert maybe is Nothing


def test_result_to_maybe_success_with_none() -> None:
    """`Success(None)` should become `Some(None)`, not `Nothing`."""
    result = Success(None)
    maybe = result_to_maybe(result)

    assert isinstance(maybe, Some)
    assert maybe.unwrap() is None
