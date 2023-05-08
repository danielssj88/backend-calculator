from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser

# read config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

def get_db_session():
    engine = create_engine(f"mysql+mysqlconnector://{config['database']['username']}:{config['database']['password']}@{config['database']['host']}:{config['database']['port']}/{config['database']['database']}")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session