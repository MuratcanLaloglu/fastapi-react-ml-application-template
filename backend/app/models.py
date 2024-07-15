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
    tokens: list["Token"] = Relationship(back_populates="user")

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

class Functions(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    model1: bool = Field(default=False)
    model2: bool = Field(default=False)
    model3: bool = Field(default=False)
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    credits: int
    models: dict[str, bool]

User.model_rebuild()
Functions.model_rebuild()