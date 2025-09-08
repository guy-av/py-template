"""Package containing disk image analyzer that extract information and metadata.

This package provides implementations for analyzing disk images. Analyzers can extract disk
information like partitions, schemes, and encryption status, as well as target-specific metadata.
"""

from abc import ABC, abstractmethod

from returns.result import ResultE

from plat_image.disk import Disk
from plat_image.info import ImageInfo


class Analyzer[T](ABC):
    """Base class for disk image analyzer.

    Generic Parameters:
        Disk: Type representing disk information extracted from image.
        Target: Type representing target-specific metadata extracted from image.
    """

    @classmethod
    @abstractmethod
    def analyze(cls, info: ImageInfo) -> ResultE[T]:
        """Analyzes an image."""
        raise NotImplementedError


class DiskAnalyzer(Analyzer[Disk], ABC):
    """Base class for disk-specific analyzer."""
