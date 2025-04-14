import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FOLDER = os.path.join(BASE_DIR, 'database')
DATABASE_PATH = os.path.join(DATABASE_FOLDER, 'database.db')
TEST_DATABASE_PATH = os.path.join(DATABASE_FOLDER, 'test_database.db')

if not os.path.exists(DATABASE_FOLDER): #pragma: no cover
    os.makedirs(DATABASE_FOLDER)

DATA_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))



class Config:
    """
    Base config
    """
    DEBUG = False
    TESTING = False
    DATABASE = DATABASE_PATH
    SWAGGER = {
        'title': 'F1 Report API',
        'version': '1.0',
        'description': 'REST API for F1 Report',
    }


class TestingConfig(Config):
    """
    Test config
    """
    TESTING = True
    DATABASE = TEST_DATABASE_PATH
