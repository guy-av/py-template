from unittest.mock import create_autospec

import pytest
from dissect.volume.disk.schemes.apm import APM
from dissect.volume.disk.schemes.bsd import BSD
from dissect.volume.disk.schemes.gpt import GPT
from dissect.volume.disk.schemes.mbr import MBR
from plat_image.analyzer.dissect import DissectDiskAnalyzer
from plat_image.disk import DiskScheme, DissectScheme
from returns.maybe import Nothing, Some
from syrupy.assertion import SnapshotAssertion

from .util import TEST_IMAGE_INFO


class TestDiskScheme:
    """Tests for the `DiskScheme` class."""

    @pytest.mark.parametrize(
        ("scheme_cls", "expected_scheme"),
        [
            (GPT, Some(DiskScheme.GPT)),
            (MBR, Some(DiskScheme.MBR)),
            (APM, Some(DiskScheme.APM)),
            (BSD, Some(DiskScheme.BSD)),
            (None, Nothing),
        ],
    )
    def test_disk_scheme(
        self,
        scheme_cls: DissectScheme | None,
        expected_scheme: DiskScheme,
    ) -> None:
        """Test the `from_obj` method."""
        scheme_obj = create_autospec(scheme_cls) if scheme_cls else None
        assert DiskScheme.from_dissect(scheme_obj) == expected_scheme


class TestDissectAnalyzer:
    """Tests for the `DissectAnalyzer` class."""

    def test_disk_analyzer(self, snapshot: SnapshotAssertion) -> None:
        """Test the `analyze_disk` method."""
        disk = DissectDiskAnalyzer.analyze(TEST_IMAGE_INFO).unwrap()
        assert disk == snapshot
