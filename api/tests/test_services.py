import pytest
from services.timezone import lookup_timezone, compute_time_data, compute_date_data
from zoneinfo import ZoneInfo

def test_lookup_timezone_valid():
    zi = lookup_timezone("US")
    assert isinstance(zi, ZoneInfo)
    assert zi.key == "America/New_York" # pytz.country_timezones['US'][0]

def test_lookup_timezone_invalid_format():
    with pytest.raises(ValueError, match="Invalid ISO code format."):
        lookup_timezone("USA")

def test_lookup_timezone_not_found():
    with pytest.raises(ValueError, match="Country code not found or has no timezones."):
        lookup_timezone("ZZ")

def test_compute_date_data():
    data = compute_date_data("US")
    assert "iso" in data
    assert data["iso"] == "US"
    assert "day" in data
    assert "month" in data
    assert "year" in data

def test_compute_time_data_12h():
    data = compute_time_data("US", format="12h")
    assert "hour" in data
    assert "meridian" in data
    assert data["meridian"] in ["AM", "PM"]

def test_compute_time_data_24h():
    data = compute_time_data("US", format="24h")
    assert "hour" in data
    assert data["meridian"] is None
