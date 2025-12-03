"""Module providing disk analysis functionality using the `dissect` library."""

from typing import override

from dissect.volume.disk import Disk as DissectDisk
from returns.maybe import Maybe
from returns.result import safe

from plat_image.analyzer import DiskAnalyzer
from plat_image.disk import Disk, DiskScheme, EncryptionType, Partition
from plat_image.info import ImageInfo


class DissectDiskAnalyzer(DiskAnalyzer):
    """Analyze disk images using the `dissect` library."""

    @staticmethod
    def __detect_encrypted_partitions(_disk: Disk) -> dict[int, EncryptionType]:
        """Detects encrypted partitions."""
        # TODO: Recognize encrypted partitions
        return {
            1: EncryptionType.BITLOCKER,
        }

    @classmethod
    @override
    @safe
    def analyze(cls, info: ImageInfo) -> Disk:
        """Analyzes a disk."""
        with info.path.open("rb") as fh:
            disk = DissectDisk(fh)
            encrypted_partitions = cls.__detect_encrypted_partitions(disk)

        return Disk(
            serial=disk.serial,
            sector_size=disk.sector_size,
            scheme=DiskScheme.from_dissect(disk.scheme),
            partitions=[
                Partition(
                    name=partition.name,
                    number=partition.number,
                    offset=partition.offset,
                    size=partition.size,
                    flags=Maybe.from_optional(partition.flags),
                    guid=Maybe.from_optional(partition.guid),
                    type=partition.type,
                    type_name=Maybe.from_optional(partition.type_str),
                    is_encrypted=partition.number in encrypted_partitions,
                    encryption_type=Maybe.from_optional(encrypted_partitions.get(partition.number)),
                )
                for partition in disk.partitions
            ],
        )
