from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

class DatabaseManager:
    __instance = None

    @staticmethod
    def get_instance():
        """Static access method."""
        if DatabaseManager.__instance is None:
            DatabaseManager()
        return DatabaseManager.__instance

    def __init__(self):
        """Virtually private constructor."""
        if DatabaseManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseManager.__instance = self
            engine = create_engine(f"mysql+mysqlconnector://{config['database']['username']}:{config['database']['password']}@{config['database']['host']}:{config['database']['port']}/{config['database']['database']}")
            self.Session = sessionmaker(bind=engine)

    def get_session(self):
        """Returns a new session."""
        return self.Session()
