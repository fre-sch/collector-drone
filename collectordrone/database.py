from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def session(config):
    engine = create_engine(config["db.url"], echo=config["db.echo"])
    Session = sessionmaker(bind=engine)
    return Session()
