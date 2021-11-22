#  Copyright (c) ZenML GmbH 2020. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

from datetime import datetime, timedelta

from hypothesis import given
from hypothesis.strategies import datetimes
from hypothesis.strategies._internal.datetime import timedeltas

from zenml.cli.utils import format_date, format_timedelta, parse_unknown_options

SAMPLE_CUSTOM_ARGUMENTS = [
    '--custom_argument="value"',
    '--food="chicken biryani"',
    '--best_cat="aria"',
]


@given(sample_datetime=datetimes(allow_imaginary=False))
def test_format_date_formats_a_string_properly(
    sample_datetime: datetime,
) -> None:
    """Check that format_date function formats a string properly"""
    # format_date(sample_datetime)
    assert isinstance(format_date(sample_datetime), str)
    assert format_date(datetime(2020, 1, 1), "%Y") == "2020"


@given(sample_timedelta=timedeltas())
def test_format_timedelta_formats_into_a_string_correctly(
    sample_timedelta: timedelta,
) -> None:
    """Check the format_timedelta function returns a formatted
    string according to specification."""
    assert isinstance(format_timedelta(sample_timedelta), str)
    assert format_timedelta(timedelta(days=1)) == "24:00:00"


def test_parse_unknown_options_returns_a_dict_of_known_options() -> None:
    """Check that parse_unknown_options returns a dict of known options"""
    parsed_sample_args = parse_unknown_options(SAMPLE_CUSTOM_ARGUMENTS)
    assert isinstance(parsed_sample_args, dict)
    assert len(parsed_sample_args.values()) == 3
    assert parsed_sample_args["best_cat"] == '"aria"'