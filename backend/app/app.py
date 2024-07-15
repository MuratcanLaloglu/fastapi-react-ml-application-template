from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from .models import User, Token, Functions, UserResponse
from .auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from .payment import router as payment_router
from services.prediction_service import PredictionService, InputData
from .dependencies import get_session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the origins you want to allow
    allow_methods=["*"],  # You can specify the methods you want to allow
    allow_headers=["*"],  # You can specify the headers you want to allow
)

app.include_router(payment_router, prefix="/api")

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    print(f"Received form data: {form_data}")  # Debug statement to print the request body
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

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == current_user.id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    functions = session.exec(select(Functions).where(Functions.id == current_user.id)).first()
    if not functions:
        functions = Functions(id=current_user.id, model1=False, model2=False, model3=False)
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        credits=user.credits,
        models={
            "model1": functions.model1,
            "model2": functions.model2,
            "model3": functions.model3,
        }
    )

@app.post("/predict/{model_name}")
async def predict_endpoint(model_name: str, input_data: InputData, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if model_name not in ["model1", "model2", "model3"]:
        raise HTTPException(status_code=400, detail="Invalid model name")

    functions = session.exec(select(Functions).where(Functions.id == current_user.id)).first()
    if not functions:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=f"Payment required for {model_name}")

    if model_name == "model1" and not functions.model1:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Payment required for model1")
    elif model_name == "model2" and not functions.model2:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Payment required for model2")
    elif model_name == "model3" and not functions.model3:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Payment required for model3")

    if model_name == "model1" and current_user.credits < 1:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Not enough credits for model1")
    elif model_name == "model2" and current_user.credits < 2:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Not enough credits for model2")
    elif model_name == "model3" and current_user.credits < 3:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Not enough credits for model3")

    prediction_service = PredictionService(model_name)
    prediction = prediction_service.predict(input_data)

    # Deduct credits based on the model used
    if model_name == "model1":
        current_user.credits -= 1
    elif model_name == "model2":
        current_user.credits -= 2
    elif model_name == "model3":
        current_user.credits -= 3

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return {"prediction": prediction["prediction"], "credits_left": current_user.credits}