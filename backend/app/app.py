from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from .models import User, Token
from .auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from .payment import router as payment_router
from services.prediction_service import PredictionService, InputData
from .dependencies import get_session

app = FastAPI()

app.include_router(payment_router, prefix="/api")

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token = Token(access_token=access_token, token_type="bearer", user_id=user.id)
    session.add(token)
    session.commit()
    session.refresh(token)
    return token

@app.post("/register", response_model=User)
async def register(user: User, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user.set_password(user.hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/predict")
async def predict_endpoint(input_data: InputData, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.credits < 1:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Not enough credits")

    prediction_service = PredictionService()
    prediction = prediction_service.predict(input_data)

    # Deduct one credit
    current_user.credits -= 1
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return {"prediction": prediction["prediction"], "credits_left": current_user.credits}