from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///data/app.db")
SessionLocal = sessionmaker(bind=engine)

def init_db() -> None:
    Base.metadata.create_all(engine)


def drop_db() -> None:
    Base.metadata.drop_all(engine)