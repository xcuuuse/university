from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

