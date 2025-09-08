"""Test suite for Image analysis behavior.

These tests verify that image analysis selects the first successful analyzer,
properly returns `Nothing` when all analyzers fail, and short-circuits on success.
"""

from typing import override
from unittest.mock import MagicMock

from plat_image import Image, analyze_image
from plat_image.analyzer import Analyzer
from plat_image.info import ImageInfo
from returns.maybe import Maybe, Nothing, Some
from returns.result import Failure, ResultE, Success
from syrupy import SnapshotAssertion

from .util import TEST_IMAGE_INFO

type MockAnalysisResult = Maybe[str]


class FakeSuccessAnalyzer(Analyzer[str]):
    """Fake analyzer that always returns a successful Maybe value."""

    RETURN_VALUE = "good"

    @classmethod
    @override
    def analyze(cls, info: ImageInfo) -> ResultE[str]:
        return Success(cls.RETURN_VALUE)


class FakeFailAnalyzer(Analyzer[str]):
    """Fake analyzer that always returns Nothing."""

    @classmethod
    @override
    def analyze(cls, info: ImageInfo) -> ResultE[str]:
        return Failure(Exception("bad"))


class TestImageAnalysis:
    """Test cases validating the behavior of image analysis and analyzer ordering."""

    def test_analyze_returns_first_success(self) -> None:
        """Ensures that the first successful analysis is returned properly."""
        analyzers = (FakeFailAnalyzer, FakeSuccessAnalyzer)

        result: MockAnalysisResult = analyze_image(TEST_IMAGE_INFO, analyzers)

        assert isinstance(result, Some)
        assert result.unwrap() == FakeSuccessAnalyzer.RETURN_VALUE

    def test_analyze_returns_nothing_if_all_fail(self) -> None:
        """Verifies that analysis returns Nothing when all analyzer fail."""
        analyzers = (FakeFailAnalyzer, FakeFailAnalyzer)

        result: MockAnalysisResult = analyze_image(TEST_IMAGE_INFO, analyzers)

        assert result == Nothing

    def test_first_success_stops_iteration(self) -> None:
        """Confirms that the first successful analysis short-circuits the process."""
        mock_fail = MagicMock()
        mock_fail.analyze.return_value = Failure(Exception("bad"))

        mock_success = MagicMock()
        mock_success.analyze.return_value = Success("good")

        mock_unused = MagicMock()

        analyzers = (mock_fail, mock_success, mock_unused)

        result: MockAnalysisResult = analyze_image(TEST_IMAGE_INFO, analyzers)

        assert result == Some("good")

        mock_fail.analyze.assert_called_once()
        mock_success.analyze.assert_called_once()
        mock_unused.analyze.assert_not_called()


class TestImage:
    """Tests for the `Image` class."""

    def test_image_creation(self, snapshot: SnapshotAssertion) -> None:
        """Test the `Image` class creation."""
        image = Image.from_info(TEST_IMAGE_INFO)
        assert image == snapshot
