from datetime import datetime
from database.models import *


def test_database(mock_report_data):

    drivers = Driver.select()
    assert len(drivers) == 2

    driver1 = Driver.get(Driver.abbreviation == "AAA")
    driver2 = Driver.get(Driver.abbreviation == "BBB")

    assert driver1.name == "Lewis"
    assert driver1.team == "MER"
    assert driver2.name == "Sebastian"
    assert driver2.team == "FER"

    results = Result.select()
    assert len(results) == 2

    result1 = Result.get(Result.driver == driver1)
    result2 = Result.get(Result.driver == driver2)

    assert result1.start_time == datetime(2025, 3, 4, 12, 1)
    assert result1.end_time == datetime(2025, 3, 4,12, 2, 30)
    assert result2.start_time == datetime(2025, 3, 4,12, 1, 10)
    assert result2.end_time == datetime(2025, 3, 4,12, 2, 40,)
