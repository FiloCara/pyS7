import pytest

from pyS7.constants import DataType, DataTypeSize, MemoryArea
from pyS7.item import Item


def test_item_creation() -> None:
    item = Item(memory_area=MemoryArea.DB, db_number=1, data_type=DataType.INT, start=10, bit_offset=0, length=1)
    assert item.memory_area == MemoryArea.DB
    assert item.db_number == 1
    assert item.data_type == DataType.INT
    assert item.start == 10
    assert item.bit_offset == 0
    assert item.length == 1

def test_size_calculation() -> None:
    item = Item(memory_area=MemoryArea.MERKER, db_number=0, data_type=DataType.REAL, start=10, bit_offset=0, length=4)
    assert item.size() == DataTypeSize[DataType.REAL] * 4

@pytest.mark.parametrize("item1, item2, result", [
    (Item(memory_area=MemoryArea.DB, db_number=1, data_type=DataType.REAL, start=0, bit_offset=0, length=1), Item(memory_area=MemoryArea.DB, db_number=1, data_type=DataType.INT, start=0, bit_offset=0, length=1), True),
    (Item(memory_area=MemoryArea.DB, db_number=1, data_type=DataType.REAL, start=0, bit_offset=0, length=1), Item(memory_area=MemoryArea.DB, db_number=1, data_type=DataType.INT, start=10, bit_offset=0, length=1), False),
    (Item(memory_area=MemoryArea.DB, db_number=1, data_type=DataType.REAL, start=0, bit_offset=0, length=1), Item(memory_area=MemoryArea.DB, db_number=1, data_type=DataType.INT, start=30, bit_offset=0, length=1), False),
    (Item(memory_area=MemoryArea.DB, db_number=1, data_type=DataType.REAL, start=0, bit_offset=0, length=1), Item(memory_area=MemoryArea.MERKER, db_number=0, data_type=DataType.BYTE, start=0, bit_offset=0, length=1), False),
])

def test_item_contains(item1: Item, item2: Item, result: bool ) -> None:
    assert item1.__contains__(item2) is result

def test_item_not_contains() -> None:
    item1 = Item(memory_area=MemoryArea.DB, db_number=1, data_type=DataType.REAL, start=20, bit_offset=0, length=1)
    item2 = Item(memory_area=MemoryArea.DB, db_number=1, data_type=DataType.INT, start=0, bit_offset=0, length=1)
    assert item1.__contains__(item2) is False

@pytest.mark.parametrize(
    "memory_area, db_number, data_type, start, bit_offset, length, exception",
    [
        ('Not Memory Area', 1, DataType.BYTE, 0, 0, 1, TypeError),          # Incorrect memory area
        (MemoryArea.DB, -1, DataType.INT, 0, 0, 1, ValueError),             # Negative db_number (<0)
        (MemoryArea.DB, 1, 'Not DataType', 0, 0, 1, TypeError),             # Incorrect datatype
        (MemoryArea.COUNTER, 0, DataType.REAL, -1, 0, 1, ValueError),       # Negative start
        (MemoryArea.INPUT, 1, DataType.DWORD, 0, 0, 1, ValueError),         # db_number must be 0
        (MemoryArea.INPUT, 0, DataType.DWORD, 0, 1, 1, ValueError),         # bit_offset must be 0
        (MemoryArea.OUTPUT, 0, DataType.BIT, 0, 0, 0, ValueError),          # length = 0
        (MemoryArea.MERKER, 'Not int', DataType.DINT, 0, 0, 1, TypeError),  # Incorrect db_number
        (MemoryArea.DB, 10, DataType.WORD, 'Not int', 0, 1, TypeError),
        (MemoryArea.DB, 2, DataType.BIT, 0, 6.5, 1, TypeError),
        (MemoryArea.DB, 2, DataType.BIT, 0, 8, 1, ValueError),
        (MemoryArea.MERKER, 0, DataType.BYTE, 0, 0, "length", TypeError),
    ],
)
def test_invalid_item_creation(memory_area, db_number, data_type, start, bit_offset, length, exception) -> None:
    with pytest.raises(exception):
        Item(memory_area=memory_area, db_number=db_number, data_type=data_type, start=start, bit_offset=bit_offset, length=length)

