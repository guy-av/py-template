"""Platform image analysis and manipulation package."""

from typing import Self

import attr
from plat_common.returns.result import result_to_maybe
from returns.maybe import Maybe, Nothing

from plat_image.analyzer import Analyzer
from plat_image.analyzer.dissect import DissectDiskAnalyzer
from plat_image.disk import Disk
from plat_image.info import ImageInfo


def analyze_image[T](info: ImageInfo, analyzers: tuple[type[Analyzer[T]], ...]) -> Maybe[T]:
    """Use the first successful analysis result from the provided analyzer."""
    for analyzer in analyzers:
        if may := result_to_maybe(analyzer.analyze(info)):
            return may

    return Nothing


@attr.s(auto_attribs=True)
class Image:
    """Represents an image."""

    disk: Maybe[Disk]

    __DISK_ANALYZERS = (DissectDiskAnalyzer,)

    @classmethod
    def from_info(cls, info: ImageInfo) -> Self:
        """Creates an image from image info."""
        return cls(
            disk=analyze_image(info, cls.__DISK_ANALYZERS),
        )
