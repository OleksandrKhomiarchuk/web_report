from peewee import (Model, CharField, ForeignKeyField,
                    SqliteDatabase, DateTimeField,
                    FloatField)
from config import DATABASE_PATH


db = SqliteDatabase(DATABASE_PATH)

class BaseModel(Model):
    class Meta:
        database = db

class Driver(BaseModel):
    abbreviation = CharField(unique=True)
    name = CharField()
    team = CharField()

class Result(BaseModel):
    driver = ForeignKeyField(Driver, backref="results")
    start_time = DateTimeField()
    end_time = DateTimeField()
    lap_time = FloatField()

def init_db():
    with db:
        db.create_tables([Driver, Result])

if __name__ == "__main__": #pragma: no cover
    init_db()
