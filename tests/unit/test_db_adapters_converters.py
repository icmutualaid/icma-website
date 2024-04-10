from datetime import date, datetime
import pytest

import blog.db


# Test our sqlite3 adapters and converters.

def test_adapter_date_iso(runner):
    test_cases = [
        {'arg': date(2020,  1,  1), 'out': '2020-01-01', },
        {'arg': date(2022,  7,  5), 'out': '2022-07-05', },
        {'arg': date(1999, 12, 31), 'out': '1999-12-31', },
    ]

    for case in test_cases:
        assert blog.db.adapt_date_iso(case['arg']) == case['out']


def test_adapter_datetime_iso(runner):
    test_cases = [
        {
            'arg': datetime(2020,  1,  1,  0,  0,  0),
            'out': '2020-01-01T00:00:00',
        },
        {
            'arg': datetime(2022,  7,  5, 17, 30,  0),
            'out': '2022-07-05T17:30:00',
        },
        {
            'arg': datetime(1999, 12, 31, 23, 59, 59),
            'out': '1999-12-31T23:59:59',
        },
    ]

    for case in test_cases:
        assert blog.db.adapt_datetime_iso(case['arg']) == case['out']


def test_adapter_datetime_epoch(runner):
    y2020 = datetime(2020, 1,   1,  0,  0,  0)
    y2022 = datetime(2022, 7,   5, 17, 30,  0)
    y1999 = datetime(1999, 12, 31, 23, 59, 59)

    test_cases = [
        {'arg': y2020, 'out': y2020.timestamp(), },
        {'arg': y2022, 'out': y2022.timestamp(), },
        {'arg': y1999, 'out': y1999.timestamp(), },
    ]

    for case in test_cases:
        assert blog.db.adapt_datetime_epoch(case['arg']) == case['out']


def test_converter_date(runner):
    test_cases = [
        {'arg': b'2020-01-01 00:00:00', 'out': date(2020,  1,  1), },
        {'arg': b'2022-07-05 17:30:00', 'out': date(2022,  7,  5), },
        {'arg': b'1999-12-31 23:59:59', 'out': date(1999, 12, 31), },
    ]

    for case in test_cases:
        assert blog.db.convert_date(case['arg']) == case['out']


def test_converter_datetime(runner):
    test_cases = [
        {
            'arg': b'2020-01-01 00:00:00',
            'out': datetime(2020,  1,  1,  0,  0,  0),
        },
        {
            'arg': b'2022-07-05 17:30:00',
            'out': datetime(2022,  7,  5, 17, 30,  0),
        },
        {
            'arg': b'1999-12-31 23:59:59',
            'out': datetime(1999, 12, 31, 23, 59, 59),
        },
    ]

    for case in test_cases:
        assert blog.db.convert_datetime(case['arg']) == case['out']


def test_converter_timestamp_datetime(runner):
    y2020 = datetime(2020, 1,   1,  0,  0,  0)
    y2022 = datetime(2022, 7,   5, 17, 30,  0)
    y1999 = datetime(1999, 12, 31, 23, 59, 59)

    def to_bytes(dt):
        return bytes(dt.strftime('%Y-%m-%d %H:%M:%S'), 'utf8')

    test_cases = [
        {'arg': to_bytes(y2020), 'out': y2020, },
        {'arg': to_bytes(y2022), 'out': y2022, },
        {'arg': to_bytes(y1999), 'out': y1999, },
        {'arg': int(y2020.timestamp()), 'out': y2020, },
        {'arg': int(y2022.timestamp()), 'out': y2022, },
        {'arg': int(y1999.timestamp()), 'out': y1999, },
    ]

    for case in test_cases:
        assert blog.db.convert_timestamp(case['arg']) == case['out']

    with pytest.raises(TypeError):
        blog.db.convert_timestamp('hello')
