from pyS7.constants import MAX_PDU, MemoryArea, DataType
from pyS7.item import Item
from pyS7.requests import ConnectionRequest, PDUNegotiationRequest, ReadRequest

def test_connection_request() -> None:
    rack = 0
    slot = 2
    connection_request = ConnectionRequest(rack=rack, slot=slot)

    expected_packet = bytearray([
        0x03, 0x00, 0x00, 0x16, 0x11, 0xe0, 0x00, 0x00, 0x00, 0x02,
        0x00, 0xc0, 0x01, 0x0a, 0xc1, 0x02, 0x01, 0x00, 0xc2, 0x02,
        0x01
    ])
    expected_packet.append(rack * 32 + slot)
    assert connection_request.request == expected_packet
    assert connection_request.serialize() == bytes(expected_packet)


def test_pdu_negotiation_request() -> None:
    pdu_negotiation_request = PDUNegotiationRequest(max_pdu=MAX_PDU)

    expected_packet = bytearray([
        0x03, 0x00, 0x00, 0x19, 0x02, 0xf0, 0x80, 0x32, 0x01, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0xf0, 0x00, 0x00,
        0x08, 0x00, 0x08, 0x03, 0xc0
    ])
    expected_packet[23:25] = MAX_PDU.to_bytes(2, byteorder="big")
    assert pdu_negotiation_request.request == expected_packet
    assert pdu_negotiation_request.serialize() == bytes(expected_packet)


def assert_read_header(packet: bytearray) -> None:
    assert packet[0] == 0x03
    assert packet[1] == 0x00
    assert packet[4] == 0x02
    assert packet[5] == 0xf0
    assert packet[6] == 0x80
    assert packet[7] == 0x32
    assert packet[8] == 0x01
    assert packet[9:11] == b'\x00\x00'
    assert packet[11:13] == b'\x00\x00'
    # assert packet[13:15] == b'\x00\x0e'
    # assert packet[15:17] == b'\x00\x00'
    assert packet[17] == 0x04
    # assert packet[18] == 0x01

def assert_read_item(packet: bytearray, offset: int, item: Item) -> None:
    assert packet[offset] == 0x12
    assert packet[offset + 1] == 0x0a
    assert packet[offset + 2] == 0x10
    assert packet[offset + 3] == item.data_type.value.to_bytes(1, byteorder='big')[0]
    assert packet[offset + 4: offset + 6] == item.length.to_bytes(2, byteorder='big')
    assert packet[offset + 6: offset + 8] == item.db_number.to_bytes(2, byteorder='big')
    assert packet[offset + 8] == item.memory_area.value
    if item.data_type == DataType.BIT:
        assert packet[offset + 9: offset + 12] == (item.start * 8 + 7 - item.bit_offset).to_bytes(3, byteorder='big')
    else:
        assert packet[offset + 9: offset + 12] == (item.start * 8 + item.bit_offset).to_bytes(3, byteorder='big')

def test_read_request():
    items = [
        Item(MemoryArea.DB, 1, DataType.BIT, 0, 6, 1),
        Item(MemoryArea.DB, 1, DataType.INT, 30, 0, 1),
        Item(MemoryArea.DB, 1, DataType.INT, 32, 0, 1),
        Item(MemoryArea.DB, 1, DataType.INT, 34, 0, 1),
        Item(MemoryArea.DB, 1, DataType.INT, 36, 0, 1),
        Item(MemoryArea.DB, 1, DataType.INT, 38, 0, 1),
        Item(MemoryArea.DB, 1, DataType.REAL, 64, 0, 1),
        Item(MemoryArea.DB, 1, DataType.REAL, 68, 0, 1),
        Item(MemoryArea.DB, 1, DataType.REAL, 72, 0, 4),
        Item(MemoryArea.DB, 1, DataType.CHAR, 102, 0, 37),
    ]

    read_request = ReadRequest(items=items)

    # Accessing the private method using the class name
    packet = read_request.request

    assert_read_header(packet)

    assert packet[2:4] == len(packet).to_bytes(2, byteorder='big')
    assert packet[13:15] == (len(packet) - 17).to_bytes(2, byteorder='big')
    assert packet[18] == len(items)

    # Validate items
    offset = 19
    for item in items:
        assert_read_item(packet, offset, item)
        offset += 12

# TODO
def assert_write_header(packet: bytearray) -> None:
    ...

# TODO
def test_write_request() -> None:
    ...