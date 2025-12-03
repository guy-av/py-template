"""Image information."""

from pathlib import Path

import attr


@attr.s(auto_attribs=True, frozen=True)
class ImageInfo:
    """Represents information about an image."""

    path: Path
