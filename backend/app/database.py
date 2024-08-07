from sqlmodel import SQLModel, create_engine
from models import User, Token, Functions

DATABASE_URL = "YOUR DATABASE URL"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()