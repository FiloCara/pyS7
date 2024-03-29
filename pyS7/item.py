from dataclasses import dataclass

from .constants import DataType, DataTypeSize, MemoryArea


@dataclass(frozen=True)
class Item:
    memory_area: MemoryArea
    db_number: int
    data_type: DataType
    start: int
    bit_offset: int
    length: int

    def __post_init__(self) -> None:
        if not isinstance(self.memory_area, MemoryArea):
            raise TypeError(
                f"Invalid memory_area: Expected type MemoryArea, \
                got {type(self.memory_area)}"
            )

        if not isinstance(self.db_number, int):
            raise TypeError(
                "Invalid db_number: Expected type int, got " + str(type(self.db_number))
            )

        if self.memory_area != MemoryArea.DB and self.db_number > 0:
            raise ValueError(
                f"Invalid db_number: Must be 0 when memory_area is {self.memory_area}, \
                  but got {self.db_number}"
            )

        if self.db_number < 0:
            raise ValueError(
                f"Invalid db_number: Expected non-negative value, got {self.db_number}"
            )

        if not isinstance(self.data_type, DataType):
            raise TypeError(
                "Invalid data_type: Expected type DataType, got "
                + str(type(self.data_type))
            )

        if not isinstance(self.start, int):
            raise TypeError(
                "Invalid start: Expected type int, got " + str(type(self.start))
            )

        if self.start < 0:
            raise ValueError(
                f"Invalid start: Expected non-negative value, got {self.start}"
            )

        if not isinstance(self.bit_offset, int):
            raise TypeError(
                f"Invalid bit_offset: Expected type int, got {type(self.bit_offset)}"
            )

        if self.data_type != DataType.BIT and self.bit_offset > 0:
            raise ValueError(
                f"Invalid bit_offset: Must be 0 when data_type is not DataType.BIT, \
                but got {self.bit_offset}"
            )

        if self.bit_offset < 0 or self.bit_offset > 7:
            raise ValueError(
                f"Invalid bit_offset: Expected value between 0 and 7, \
                  got {self.bit_offset}"
            )

        if not isinstance(self.length, int):
            raise TypeError(
                "Invalid length: Expected type int, got " + str(type(self.length))
            )

        if self.length <= 0:
            raise ValueError(
                f"Invalid length: Expected positive value, got {self.length}"
            )

    def size(self) -> int:
        """Return the Item size in bytes"""
        return DataTypeSize[self.data_type] * self.length

    def __contains__(self, item) -> bool:  # type: ignore
        if (
            self.memory_area == item.memory_area
            and self.db_number == item.db_number
            and self.start <= item.start
            and self.start + DataTypeSize[self.data_type] * self.length
            >= item.start + DataTypeSize[item.data_type] * item.length
        ):
            return True
        return False
