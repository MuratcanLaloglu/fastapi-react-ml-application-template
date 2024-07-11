from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class InputData(BaseModel):
    married: float
    income: float
    education: float
    loan_amount: float
    credit_history: float


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    credits: int = Field(default=0)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)


class Token(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    access_token: str
    token_type: str
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="tokens")


User.model_rebuild()
