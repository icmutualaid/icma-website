import datetime
import pytest

import blog.db


# Test our sqlite3 adapters and converters.

def test_adapter_date_iso(runner):
    test_cases = [
        {'arg': datetime.date(2020,  1,  1), 'out': '2020-01-01', },
        {'arg': datetime.date(2022,  7,  5), 'out': '2022-07-05', },
        {'arg': datetime.date(1999, 12, 31), 'out': '1999-12-31', },
    ]

    for case in test_cases:
        assert blog.db.adapt_date_iso(case['arg']) == case['out']


def test_adapter_datetime_iso(runner):
    test_cases = [
        {
            'arg': datetime.datetime(2020,  1,  1,  0,  0,  0),
            'out': '2020-01-01T00:00:00',
        },
        {
            'arg': datetime.datetime(2022,  7,  5, 17, 30,  0),
            'out': '2022-07-05T17:30:00',
        },
        {
            'arg': datetime.datetime(1999, 12, 31, 23, 59, 59),
            'out': '1999-12-31T23:59:59',
        },
    ]

    for case in test_cases:
        assert blog.db.adapt_datetime_iso(case['arg']) == case['out']


def test_adapter_datetime_epoch(runner):
    test_cases = [
        {
            'arg': datetime.datetime(2020,  1,  1,  0,  0,  0),
            'out': 1577858400,
        },
        {
            'arg': datetime.datetime(2022,  7,  5, 17, 30,  0),
            'out': 1657060200,
        },
        {
            'arg': datetime.datetime(1999, 12, 31, 23, 59, 59),
            'out': 946706399,
        },
    ]

    for case in test_cases:
        assert blog.db.adapt_datetime_epoch(case['arg']) == case['out']


def test_converter_date(runner):
    test_cases = [
        {'arg': b'2020-01-01 00:00:00', 'out': datetime.date(2020,  1,  1), },
        {'arg': b'2022-07-05 17:30:00', 'out': datetime.date(2022,  7,  5), },
        {'arg': b'1999-12-31 23:59:59', 'out': datetime.date(1999, 12, 31), },
    ]

    for case in test_cases:
        assert blog.db.convert_date(case['arg']) == case['out']


def test_converter_datetime(runner):
    test_cases = [
        {
            'arg': b'2020-01-01 00:00:00',
            'out': datetime.datetime(2020,  1,  1,  0,  0,  0),
        },
        {
            'arg': b'2022-07-05 17:30:00',
            'out': datetime.datetime(2022,  7,  5, 17, 30,  0),
        },
        {
            'arg': b'1999-12-31 23:59:59',
            'out': datetime.datetime(1999, 12, 31, 23, 59, 59),
        },
    ]

    for case in test_cases:
        assert blog.db.convert_datetime(case['arg']) == case['out']


def test_converter_timestamp_datetime(runner):
    test_cases = [
        {
            'arg': b'2020-01-01 00:00:00',
            'out': datetime.datetime(2020,  1,  1,  0,  0,  0),
        },
        {
            'arg': b'2022-07-05 17:30:00',
            'out': datetime.datetime(2022,  7,  5, 17, 30,  0),
        },
        {
            'arg': b'1999-12-31 23:59:59',
            'out': datetime.datetime(1999, 12, 31, 23, 59, 59),
        },
        {
            'arg': 1577858400,
            'out': datetime.datetime(2020,  1,  1,  0,  0,  0),
        },
        {
            'arg': 1657060200,
            'out': datetime.datetime(2022,  7,  5, 17, 30,  0),
        },
        {
            'arg': 946706399,
            'out': datetime.datetime(1999, 12, 31, 23, 59, 59),
        },
    ]

    for case in test_cases:
        assert blog.db.convert_timestamp(case['arg']) == case['out']

    with pytest.raises(TypeError):
        blog.db.convert_timestamp('hello')
