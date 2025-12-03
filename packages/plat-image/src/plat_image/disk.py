"""This module contains data models for representing disk information in the platform analyzer."""

from enum import Enum
from typing import Self
from uuid import UUID

import attr
from dissect.volume.disk.schemes.apm import APM
from dissect.volume.disk.schemes.bsd import BSD
from dissect.volume.disk.schemes.gpt import GPT
from dissect.volume.disk.schemes.mbr import MBR
from returns.maybe import Maybe, Nothing, Some


class EncryptionType(Enum):
    """Represents a type of encryption."""

    BITLOCKER = "BitLocker"

    UNKNOWN = "unknown"


@attr.s(auto_attribs=True)
class Partition:
    """Represents a partition in a platform."""

    name: str
    number: int

    offset: int
    size: int

    flags: Maybe[int]

    guid: Maybe[UUID]
    type: UUID | int

    type_name: Maybe[str]

    is_encrypted: bool
    encryption_type: Maybe[EncryptionType]


type DissectScheme = GPT | MBR | APM | BSD


class DiskScheme(Enum):
    """Represents a disk scheme."""

    GPT = "gpt"
    MBR = "mbr"
    APM = "apm"
    BSD = "bsd"

    @classmethod
    def from_dissect(cls, obj: DissectScheme | None) -> Maybe[Self]:
        """Converts a dissect scheme to a plat scheme."""
        match obj:
            case GPT():
                return Some(cls.GPT)

            case MBR():
                return Some(cls.MBR)

            case APM():
                return Some(cls.APM)

            case BSD():
                return Some(cls.BSD)

        return Nothing


@attr.s(auto_attribs=True, frozen=True)
class Disk:
    """Represents a disk in a platform."""

    serial: Maybe[int]
    sector_size: int
    scheme: Maybe[DiskScheme]
    partitions: Maybe[list[Partition]]
