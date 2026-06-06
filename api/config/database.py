from fastapi import Depends
from sqlalchemy.sql.annotation import Annotated
from sqlmodel import Session, create_engine

sqlite_name: str = "db.sqlite3"
sqlite_url: str = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url)


def get_session():
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]
