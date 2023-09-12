from collections import namedtuple

import pytest

from pyS7.constants import DataType, MemoryArea
from pyS7.item import Item
from pyS7.responses import (
    ConnectionResponse,
    PDUNegotiationResponse,
    ReadOptimizedResponse,
    ReadResponse,
    parse_optimized_read_response,
    parse_read_response,
)


def test_conenction_response() -> None:
    bytes_response = b""

    connection_response = ConnectionResponse(response=bytes_response)
    assert connection_response.response == bytes_response


@pytest.mark.parametrize(
    "bytes_response, max_jobs_calling, max_jobs_called, pdu_size",
    [
        (
            b"\x03\x00\x00\x1b\x02\xf0\x802\x03\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\xf0\x00\x00\x08\x00\x08\x03\xc0",
            8,
            8,
            960,
        ),
        (
            b"\x03\x00\x00\x1b\x02\xf0\x802\x03\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\xf0\x00\x00\x04\x00\x04\x00\xf0",
            4,
            4,
            240,
        ),
    ],
)
def test_pdu_negotiation_response(
    bytes_response: bytes, max_jobs_calling: int, max_jobs_called: int, pdu_size: int
) -> None:
    pdu_negotiation_response = PDUNegotiationResponse(response=bytes_response)

    assert pdu_negotiation_response.response == bytes_response
    (
        negotiated_max_jobs_calling,
        negotiated_max_jobs_called,
        negotiated_pdu_size,
    ) = pdu_negotiation_response.parse()

    assert negotiated_max_jobs_calling == max_jobs_calling
    assert negotiated_max_jobs_called == max_jobs_called
    assert negotiated_pdu_size == pdu_size


ReadResponseTestCase = namedtuple(
    "ReadResponseTestCase", ["bytes_response", "items", "parsed_values"]
)
read_response_test_cases: list[ReadResponseTestCase] = [
    ReadResponseTestCase(
        b"\x03\x00\x00\x97\x02\xf0\x802\x03\x00\x00\x00\x00\x00\x02\x00\x82\x00\x00\x04\x14\xff\x03\x00\x01\x01\x00\xff\x03\x00\x01\x01\x00\xff\x03\x00\x01\x01\x00\xff\x03\x00\x01\x00\x00\xff\x03\x00\x01\x01\x00\xff\x03\x00\x01\x00\x08\xff\x03\x00\x01\x01\x00\xff\x03\x00\x01\x00\x00\xff\x04\x00\x08\x00\xfd\xff\x04\x00\x08\xff\x00\xff\x05\x00\x10\x80\x00\xff\x05\x00\x10\xfb.\xff\x05\x00\x10\x00\x00\xff\x05\x00\x10\x04\xd2\xff\x05\x00\x10\x7f\xff\xff\x05\x00 \x80\x00\x00\x00\xff\x05\x00 \xff\xff\x80\x00\xff\x05\x00 \x00\x00\x00\x00\xff\x05\x00 \x00\x00\x7f\xff\xff\x05\x00 \x7f\xff\xff\xff",
        [
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 0, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 1, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 2, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 3, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 4, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 5, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 6, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 7, 1),
            Item(MemoryArea.DB, 1, DataType.BYTE, 20, 0, 1),
            Item(MemoryArea.DB, 1, DataType.BYTE, 21, 0, 1),
            Item(MemoryArea.DB, 1, DataType.INT, 30, 0, 1),
            Item(MemoryArea.DB, 1, DataType.INT, 32, 0, 1),
            Item(MemoryArea.DB, 1, DataType.INT, 34, 0, 1),
            Item(MemoryArea.DB, 1, DataType.INT, 36, 0, 1),
            Item(MemoryArea.DB, 1, DataType.INT, 38, 0, 1),
            Item(MemoryArea.DB, 1, DataType.DINT, 40, 0, 1),
            Item(MemoryArea.DB, 1, DataType.DINT, 44, 0, 1),
            Item(MemoryArea.DB, 1, DataType.DINT, 48, 0, 1),
            Item(MemoryArea.DB, 1, DataType.DINT, 52, 0, 1),
            Item(MemoryArea.DB, 1, DataType.DINT, 56, 0, 1),
        ],
        [
            True,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            0,
            255,
            -32768,
            -1234,
            0,
            1234,
            32767,
            -2147483648,
            -32768,
            0,
            32767,
            2147483647,
        ],
    ),
    ReadResponseTestCase(
        b"\x03\x00\x00\xe1\x02\xf0\x802\x03\x00\x00\x00\x00\x00\x02\x00\xcc\x00\x00\x04\x14\xff\x07\x00\x04\xff\x7f\xff\xfd\xff\x07\x00\x04\xd4F\x12\x04\xff\x07\x00\x04\x8e\x0e`\xc0\xff\x07\x00\x04\xab\xa5o\xa6\xff\x07\x00\x04\x00\x00\x00\x00\xff\x07\x00\x04\x00\x80\x00\x00\xff\x07\x00\x04+\xa5o\xa6\xff\x07\x00\x04TF\x12\x05\xff\x07\x00\x04\x7f\x7f\xff\xff\xff\t\x00\x15the brown fox jumps o\x00\xff\t\x00,the brown fox jumps over the lazy dog, hello\xff\x04\x00\x10\x00\x00\xff\x04\x00\x10\x00\x00\xff\x04\x00\x10\x124\xff\x04\x00\x10\x00\x00\xff\x04\x00\x10\xab\xcd\xff\x04\x00\x10\x00\x00\xff\x04\x00\x10\xff\xff\xff\x04\x00 \x00\x00\x00\x00\xff\x04\x00 \x00\x00\x00\x00",
        [
            Item(MemoryArea.DB, 1, DataType.REAL, 60, 0, 1),
            Item(MemoryArea.DB, 1, DataType.REAL, 64, 0, 1),
            Item(MemoryArea.DB, 1, DataType.REAL, 68, 0, 1),
            Item(MemoryArea.DB, 1, DataType.REAL, 72, 0, 1),
            Item(MemoryArea.DB, 1, DataType.REAL, 76, 0, 1),
            Item(MemoryArea.DB, 1, DataType.REAL, 80, 0, 1),
            Item(MemoryArea.DB, 1, DataType.REAL, 84, 0, 1),
            Item(MemoryArea.DB, 1, DataType.REAL, 88, 0, 1),
            Item(MemoryArea.DB, 1, DataType.REAL, 92, 0, 1),
            Item(MemoryArea.DB, 1, DataType.CHAR, 102, 0, 21),
            Item(MemoryArea.DB, 1, DataType.CHAR, 102, 0, 44),
            Item(MemoryArea.DB, 1, DataType.WORD, 200, 0, 1),
            Item(MemoryArea.DB, 1, DataType.WORD, 202, 0, 1),
            Item(MemoryArea.DB, 1, DataType.WORD, 204, 0, 1),
            Item(MemoryArea.DB, 1, DataType.WORD, 206, 0, 1),
            Item(MemoryArea.DB, 1, DataType.WORD, 208, 0, 1),
            Item(MemoryArea.DB, 1, DataType.WORD, 210, 0, 1),
            Item(MemoryArea.DB, 1, DataType.WORD, 212, 0, 1),
            Item(MemoryArea.DB, 1, DataType.DWORD, 300, 0, 1),
            Item(MemoryArea.DB, 1, DataType.DWORD, 304, 0, 1),
        ],
        [
            -3.4028230607370965e38,
            -3402823106560.0,
            -1.7549434765121066e-30,
            -1.1754943806535634e-12,
            0.0,
            1.1754943508222875e-38,
            1.1754943806535634e-12,
            3402823368704.0,
            3.4028234663852886e38,
            "the brown fox jumps o",
            "the brown fox jumps over the lazy dog, hello",
            0,
            0,
            4660,
            0,
            43981,
            0,
            65535,
            0,
            0,
        ],
    ),
    ReadResponseTestCase(
        b"\x03\x00\x00=\x02\xf0\x802\x03\x00\x00\x00\x00\x00\x02\x00(\x00\x00\x04\x05\xff\x04\x00 \x124Vx\xff\x04\x00 \x00\x00\x00\x00\xff\x04\x00 \x124\xab\xcd\xff\x04\x00 \x00\x00\x00\x00\xff\x04\x00 \xff\xff\xff\xff",
        [
            Item(MemoryArea.DB, 1, DataType.DWORD, 308, 0, 1),
            Item(MemoryArea.DB, 1, DataType.DWORD, 312, 0, 1),
            Item(MemoryArea.DB, 1, DataType.DWORD, 316, 0, 1),
            Item(MemoryArea.DB, 1, DataType.DWORD, 320, 0, 1),
            Item(MemoryArea.DB, 1, DataType.DWORD, 324, 0, 1),
        ],
        [305419896, 0, 305441741, 0, 4294967295],
    ),
    ReadResponseTestCase(
        b"\x03\x00\x00\x83\x02\xf0\x802\x03\x00\x00\x00\x00\x00\x02\x00n\x00\x00\x04\x10\xff\x03\x00\x01\x01\x00\xff\x03\x00\x01\x01\x00\xff\x03\x00\x01\x01\x00\xff\x03\x00\x01\x00\x00\xff\x03\x00\x01\x01\x00\xff\x03\x00\x01\x00\x08\xff\x03\x00\x01\x01\x00\xff\x03\x00\x01\x00\x00\xff\x04\x00\x08\x00\x00\xff\x04\x00\x08\xff\x00\xff\x05\x00\x10\x80\x00\xff\x05\x00\x10\xfb.\xff\x05\x00\x10\x00\x00\xff\x05\x00\x10\x04\xd2\xff\x05\x00\x10\x7f\xff\xff\x05\x00\x80\x80\x00\x00\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x7f\xff",
        [
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 0, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 1, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 2, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 3, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 4, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 5, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 6, 1),
            Item(MemoryArea.DB, 1, DataType.BIT, 0, 7, 1),
            Item(MemoryArea.DB, 1, DataType.BYTE, 20, 0, 1),
            Item(MemoryArea.DB, 1, DataType.BYTE, 21, 0, 1),
            Item(MemoryArea.DB, 1, DataType.INT, 30, 0, 1),
            Item(MemoryArea.DB, 1, DataType.INT, 32, 0, 1),
            Item(MemoryArea.DB, 1, DataType.INT, 34, 0, 1),
            Item(MemoryArea.DB, 1, DataType.INT, 36, 0, 1),
            Item(MemoryArea.DB, 1, DataType.INT, 38, 0, 1),
            Item(MemoryArea.DB, 2, DataType.DINT, 40, 0, 4),
        ],
        [
            True,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            0,
            255,
            -32768,
            -1234,
            0,
            1234,
            32767,
            (-2147483648, -32768, 0, 32767),
        ],
    ),
]


@pytest.mark.parametrize("test_case", read_response_test_cases)
def test_parse_read_response(test_case: ReadResponseTestCase) -> None:
    assert (
        parse_read_response(
            bytes_response=test_case.bytes_response, items=test_case.items
        )
        == test_case.parsed_values
    )


@pytest.mark.parametrize("test_case", read_response_test_cases)
def test_read_response(test_case: ReadResponseTestCase) -> None:
    read_response = ReadResponse(
        response=test_case.bytes_response, items=test_case.items
    )

    assert read_response.response == test_case.bytes_response
    assert read_response.items == test_case.items
    assert read_response.parse() == test_case.parsed_values


ReadResponseOptimizedTestCase = namedtuple(
    "ReadResponseOptimizedTestCase", ["bytes_response", "items_map", "parsed_values"]
)
read_response_optimized_test_case: list[ReadResponseOptimizedTestCase] = [
    ReadResponseOptimizedTestCase(
        [
            b"\x03\x00\x00\xcf\x02\xf0\x802\x03\x00\x00\x00\x00\x00\x02\x00\xba\x00\x00\x04\x04\xff\x04\x00\x08\xea\x00\xff\x04\x03\xf0\x00\xff\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\xfb.\x00\x00\x04\xd2\x7f\xff\x80\x00\x00\x00\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x7f\xff\x7f\xff\xff\xff\xff\x7f\xff\xfd\xd4F\x12\x04\x8e\x0e`\xc0\xab\xa5o\xa6\x00\x00\x00\x00\x00\x80\x00\x00+\xa5o\xa6TF\x12\x05\x7f\x7f\xff\xff\x00\x00\x00\x00\xfe,the brown fox jumps over the lazy dog, hello\xff\x04\x00p\x00\x00\x00\x00\x124\x00\x00\xab\xcd\x00\x00\xff\xff\xff\x04\x00\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x124Vx\x00\x00\x00\x00\x124\xab\xcd\x00\x00\x00\x00\xff\xff\xff\xff"
        ],
        [
            {
                Item(MemoryArea.DB, 1, DataType.BYTE, 0, 0, 1): [
                    (0, Item(MemoryArea.DB, 1, DataType.BIT, 0, 0, 1)),
                    (1, Item(MemoryArea.DB, 1, DataType.BIT, 0, 1, 1)),
                    (2, Item(MemoryArea.DB, 1, DataType.BIT, 0, 2, 1)),
                    (3, Item(MemoryArea.DB, 1, DataType.BIT, 0, 3, 1)),
                    (4, Item(MemoryArea.DB, 1, DataType.BIT, 0, 4, 1)),
                    (5, Item(MemoryArea.DB, 1, DataType.BIT, 0, 5, 1)),
                    (6, Item(MemoryArea.DB, 1, DataType.BIT, 0, 6, 1)),
                    (7, Item(MemoryArea.DB, 1, DataType.BIT, 0, 7, 1)),
                ],
                Item(MemoryArea.DB, 1, DataType.BYTE, 20, 0, 126): [
                    (8, Item(MemoryArea.DB, 1, DataType.BYTE, 20, 0, 1)),
                    (9, Item(MemoryArea.DB, 1, DataType.BYTE, 21, 0, 1)),
                    (10, Item(MemoryArea.DB, 1, DataType.INT, 30, 0, 1)),
                    (11, Item(MemoryArea.DB, 1, DataType.INT, 32, 0, 1)),
                    (12, Item(MemoryArea.DB, 1, DataType.INT, 34, 0, 1)),
                    (13, Item(MemoryArea.DB, 1, DataType.INT, 36, 0, 1)),
                    (14, Item(MemoryArea.DB, 1, DataType.INT, 38, 0, 1)),
                    (15, Item(MemoryArea.DB, 1, DataType.DINT, 40, 0, 1)),
                    (16, Item(MemoryArea.DB, 1, DataType.DINT, 44, 0, 1)),
                    (17, Item(MemoryArea.DB, 1, DataType.DINT, 48, 0, 1)),
                    (18, Item(MemoryArea.DB, 1, DataType.DINT, 52, 0, 1)),
                    (19, Item(MemoryArea.DB, 1, DataType.DINT, 56, 0, 1)),
                    (20, Item(MemoryArea.DB, 1, DataType.REAL, 60, 0, 1)),
                    (21, Item(MemoryArea.DB, 1, DataType.REAL, 64, 0, 1)),
                    (22, Item(MemoryArea.DB, 1, DataType.REAL, 68, 0, 1)),
                    (23, Item(MemoryArea.DB, 1, DataType.REAL, 72, 0, 1)),
                    (24, Item(MemoryArea.DB, 1, DataType.REAL, 76, 0, 1)),
                    (25, Item(MemoryArea.DB, 1, DataType.REAL, 80, 0, 1)),
                    (26, Item(MemoryArea.DB, 1, DataType.REAL, 84, 0, 1)),
                    (27, Item(MemoryArea.DB, 1, DataType.REAL, 88, 0, 1)),
                    (28, Item(MemoryArea.DB, 1, DataType.REAL, 92, 0, 1)),
                    (29, Item(MemoryArea.DB, 1, DataType.CHAR, 102, 0, 21)),
                    (30, Item(MemoryArea.DB, 1, DataType.CHAR, 102, 0, 44)),
                ],
                Item(MemoryArea.DB, 1, DataType.BYTE, 200, 0, 14): [
                    (31, Item(MemoryArea.DB, 1, DataType.WORD, 200, 0, 1)),
                    (32, Item(MemoryArea.DB, 1, DataType.WORD, 202, 0, 1)),
                    (33, Item(MemoryArea.DB, 1, DataType.WORD, 204, 0, 1)),
                    (34, Item(MemoryArea.DB, 1, DataType.WORD, 206, 0, 1)),
                    (35, Item(MemoryArea.DB, 1, DataType.WORD, 208, 0, 1)),
                    (36, Item(MemoryArea.DB, 1, DataType.WORD, 210, 0, 1)),
                    (37, Item(MemoryArea.DB, 1, DataType.WORD, 212, 0, 1)),
                ],
                Item(MemoryArea.DB, 1, DataType.BYTE, 300, 0, 28): [
                    (38, Item(MemoryArea.DB, 1, DataType.DWORD, 300, 0, 1)),
                    (39, Item(MemoryArea.DB, 1, DataType.DWORD, 304, 0, 1)),
                    (40, Item(MemoryArea.DB, 1, DataType.DWORD, 308, 0, 1)),
                    (41, Item(MemoryArea.DB, 1, DataType.DWORD, 312, 0, 1)),
                    (42, Item(MemoryArea.DB, 1, DataType.DWORD, 316, 0, 1)),
                    (43, Item(MemoryArea.DB, 1, DataType.DWORD, 320, 0, 1)),
                    (44, Item(MemoryArea.DB, 1, DataType.DWORD, 324, 0, 1)),
                ],
            }
        ],
        [
            True,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            0,
            255,
            -32768,
            -1234,
            0,
            1234,
            32767,
            -2147483648,
            -32768,
            0,
            32767,
            2147483647,
            -3.4028230607370965e38,
            -3402823106560.0,
            -1.7549434765121066e-30,
            -1.1754943806535634e-12,
            0.0,
            1.1754943508222875e-38,
            1.1754943806535634e-12,
            3402823368704.0,
            3.4028234663852886e38,
            "the brown fox jumps o",
            "the brown fox jumps over the lazy dog, hello",
            0,
            0,
            4660,
            0,
            43981,
            0,
            65535,
            0,
            0,
            305419896,
            0,
            305441741,
            0,
            4294967295,
        ],
    )
]


@pytest.mark.parametrize("test_case", read_response_optimized_test_case)
def test_parse_optimized_read_response(
    test_case: ReadResponseOptimizedTestCase,
) -> None:
    assert (
        parse_optimized_read_response(
            bytes_responses=test_case.bytes_response, items_map=test_case.items_map
        )
        == test_case.parsed_values
    )


@pytest.mark.parametrize("test_case", read_response_optimized_test_case)
def test_read_optimized_response(test_case: ReadResponseTestCase) -> None:
    read_response = ReadOptimizedResponse(
        response=test_case.bytes_response[0], item_map=test_case.items_map[0]
    )

    assert read_response.responses == test_case.bytes_response
    assert read_response.items_map == test_case.items_map
    assert read_response.n_messages == 1
    assert read_response.parse() == test_case.parsed_values

