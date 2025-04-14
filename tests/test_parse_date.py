from unittest.mock import patch
from database.parse_data import store_data_in_db
from database.models import Driver, Result
from datetime import datetime


def mock_parse_logs(folder_path):
    return {
        'start_times': {
            'AAA': datetime(2025, 3, 4, 12, 1, 0),
            'BBB': datetime(2025, 3, 4, 12, 1, 10)
        },
        'end_times': {
            'AAA': datetime(2025, 3, 4, 12, 2, 30),
            'BBB': datetime(2025, 3, 4, 12, 2, 40)
        }
    }


def mock_calculate_lap_times(data):
    return [
        {'abbreviation': 'AAA', 'name': 'Lewis', 'team': 'MER', 'formatted_lap_time': '00:01:30'},
        {'abbreviation': 'BBB', 'name': 'Sebastian', 'team': 'FER', 'formatted_lap_time': '00:01:30'}
    ]

def test_store_data_in_db(client):
    with patch('database.parse_data.parse_logs',
               side_effect=mock_parse_logs) as mock_parse, \
            patch('database.parse_data.calculate_lap_times',
                  side_effect=mock_calculate_lap_times) as mock_calc:
        store_data_in_db('mock_folder')
        assert Driver.select().count() == 2
        assert Result.select().count() == 2
        driver_aaa = Driver.get(Driver.abbreviation == 'AAA')
        driver_bbb = Driver.get(Driver.abbreviation == 'BBB')
        assert driver_aaa.name == 'Lewis'
        assert driver_aaa.team == 'MER'
        assert driver_bbb.name == 'Sebastian'
        assert driver_bbb.team == 'FER'
        result_aaa = Result.get(Result.driver == driver_aaa)
        result_bbb = Result.get(Result.driver == driver_bbb)
        assert str(result_aaa.start_time) == '2025-03-04 12:01:00'
        assert str(result_aaa.end_time) == '2025-03-04 12:02:30'
        assert str(result_bbb.start_time) == '2025-03-04 12:01:10'
        assert str(result_bbb.end_time) == '2025-03-04 12:02:40'
