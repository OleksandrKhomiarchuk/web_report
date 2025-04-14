import sys, os, pytest
from app import create_app
from database.models import *
from config import TEST_DATABASE_PATH
from peewee import SqliteDatabase


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
test_db = SqliteDatabase(TEST_DATABASE_PATH)

@pytest.fixture(scope="function")
def client():
    app = create_app("TestingConfig")
    app.config["SERVER_NAME"] = "localhost"
    db.init(TEST_DATABASE_PATH)
    db.bind([Driver, Result])
    db.connect(reuse_if_open=True)
    db.create_tables([Driver, Result])
    with app.test_client() as c:
        with app.app_context():
            yield c
    db.drop_tables([Driver, Result])
    db.close()

@pytest.fixture(scope="function")
def mock_report_data(client):
    with db.atomic():
        driver1 = Driver.create(abbreviation="AAA", name="Lewis", team="MER")
        driver2 = Driver.create(abbreviation="BBB", name="Sebastian", team="FER")

        Result.create(
            driver=driver1,
            start_time="2025-03-04 12:01:00",
            end_time="2025-03-04 12:02:30",
            lap_time="00:01:30"
        )
        Result.create(
            driver=driver2,
            start_time="2025-03-04 12:01:10",
            end_time="2025-03-04 12:02:40",
            lap_time="00:01:30"
        )

    yield
    with db.atomic(): #pragma: no cover
        if db.table_exists("result"):
            Result.delete().where(True).execute()
        if db.table_exists("driver"):
            Driver.delete().where(True).execute()
