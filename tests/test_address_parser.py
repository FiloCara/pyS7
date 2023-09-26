import pytest

import pyS7
from pyS7.address_parser import map_address_to_item
from pyS7.constants import DataType, MemoryArea
from pyS7.item import Item


@pytest.mark.parametrize("test_input, expected",
    [
        ("DB50,X0.7",  Item(MemoryArea.DB, 50, DataType.BIT, 0, 7, 1)),
        ("DB23,B1",    Item(MemoryArea.DB, 23, DataType.BYTE, 1, 0, 1)),
        ("db12,R5",    Item(MemoryArea.DB, 12, DataType.REAL, 5, 0, 1)),
        ("DB100,C2",   Item(MemoryArea.DB, 100, DataType.CHAR, 2, 0, 1)),
        ("DB42,I3",    Item(MemoryArea.DB, 42, DataType.INT, 3, 0, 1)),
        ("DB57,WORD4", Item(MemoryArea.DB, 57, DataType.WORD, 4, 0, 1)),
        ("DB13,DI5",   Item(MemoryArea.DB, 13, DataType.DINT, 5, 0, 1)),
        ("DB19,DW6",   Item(MemoryArea.DB, 19, DataType.DWORD, 6, 0, 1)),
        ("DB21,R7",    Item(MemoryArea.DB, 21, DataType.REAL, 7, 0, 1)),
        ("DB2,S7.10",  Item(MemoryArea.DB, 2, DataType.CHAR, 7, 0, 10)),
        ("M10.7",      Item(MemoryArea.MERKER, 0, DataType.BIT, 10, 7, 1)),
        ("I0.2",       Item(MemoryArea.INPUT, 0, DataType.BIT, 0, 2, 1)),
        ("Q300.1",     Item(MemoryArea.OUTPUT, 0, DataType.BIT, 300, 1, 1)),
        ("QB20",       Item(MemoryArea.OUTPUT, 0, DataType.BYTE, 20, 0, 1)),
        ("MW320",      Item(MemoryArea.MERKER, 0, DataType.WORD, 320, 0, 1))
    ]
)
def test_map_address_to_item(test_input, expected) -> None:
    assert map_address_to_item(address=test_input) == expected


@pytest.mark.parametrize("test_input, exception",
    [
        ("DB12,X10", pyS7.errors.AddressError),     # Missing bit offset
        ("DB12,X10.8", pyS7.errors.AddressError),   # Invalid bit offset
        ("DB12,W22.6", pyS7.errors.AddressError),   # Invalid bit offset
        ("DB12,DI40.1", pyS7.errors.AddressError),  # Invalid bit offset
        ("DB53,DW5.5", pyS7.errors.AddressError),   # Invalid bit offset
        ("DB24,R102.4", pyS7.errors.AddressError),  # Invalid bit offset
        ("I10.11", pyS7.errors.AddressError),       # Invalid bit offset
        ("A1.17", pyS7.errors.AddressError),        # Invalid bit offset
        ("M3.9", pyS7.errors.AddressError),         # Invalid bit offset
        ("DB12,S102", pyS7.errors.AddressError),    # Missing length
        ("DT23", pyS7.errors.AddressError),         # Invalid address
        ("DB1,FLOAT10", pyS7.errors.AddressError),  # FLOAT not good, use REAL instead
        ("DB56,B11.5", pyS7.errors.AddressError),   # Unsupported bit offset for type BYTE
        ("DB1,CHAR11.5", pyS7.errors.AddressError), # Unsupported bit offset for type CHAR
        ("DB30,I0.5", pyS7.errors.AddressError),    # Unsupported bit offset for type INT
        ("DBX50.1", pyS7.errors.AddressError),      # Wrong format
        ("DB50.DBX50.1", pyS7.errors.AddressError), # Wrong format
        ("DB16,DC5", pyS7.errors.AddressError),     # Wrong format
        ("I1,10", pyS7.errors.AddressError),        # Wrong format
        ("M1?10", pyS7.errors.AddressError),        # Wrong format
        ("Q25?10,9", pyS7.errors.AddressError),     # Wrong format
        ("IEU,90", pyS7.errors.AddressError),       # Wrong format
        ("QZ,21", pyS7.errors.AddressError),        # Wrong format
        ("MUN21", pyS7.errors.AddressError),        # Wrong format
    ]
)
def test_invalid_address(test_input, exception) -> None:
    with pytest.raises(exception):
        map_address_to_item(test_input)
