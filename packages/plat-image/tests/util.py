from pathlib import Path

from plat_image.info import ImageInfo

RESOURCES_DIR = Path(__file__).parent / "resources"
TEST_IMAGE = RESOURCES_DIR / "test-image.dd"
TEST_IMAGE_INFO = ImageInfo(
    path=TEST_IMAGE,
)
