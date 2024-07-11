from sqlmodel import Session, create_engine

DATABASE_URL = "postgresql://postgres:2534@localhost/mina"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session