from sqlmodel import create_engine, Session

from credentials import SQL_PATH

engine = create_engine(SQL_PATH, echo=True)

def get_session():
    with Session(engine) as session:
        yield session