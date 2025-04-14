from config import DATA_FOLDER
from database.models import db, Driver, Result
from f1_report_by_viacent.functions import parse_logs, calculate_lap_times


def store_data_in_db(folder_path):
    """
    Reads data from files and stores them in the database.
    """
    Result.delete().execute()
    Driver.delete().execute()

    data = parse_logs(folder_path)
    lap_times = calculate_lap_times(data)
    existing_drivers = {d.abbreviation: d for d in Driver.select()}
    new_drivers = [
        Driver(
            abbreviation = entry['abbreviation'],
            name = entry['name'],
            team = entry['team']
        )
        for entry in lap_times if entry['abbreviation'] not in existing_drivers
    ]
    if new_drivers:
        Driver.bulk_create(new_drivers)
        existing_drivers.update({d.abbreviation: d for d in Driver.select()})
    result = [
        Result(
            driver = existing_drivers[entry['abbreviation']],
            start_time = data['start_times'][entry['abbreviation']],
            end_time = data['end_times'][entry['abbreviation']],
            lap_time = entry['formatted_lap_time']
        )
        for entry in lap_times
    ]
    Result.bulk_create(result)


if __name__ == "__main__": #pragma: no cover
    db.connect()
    db.create_tables([Driver, Result])
    store_data_in_db(DATA_FOLDER)