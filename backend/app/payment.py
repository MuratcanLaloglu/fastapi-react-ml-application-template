from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from .models import User, Functions
from .auth import get_current_user
from .dependencies import get_session

router = APIRouter()

@router.post("/payment/{model_name}")
async def process_payment(model_name: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if model_name not in ["model1", "model2", "model3"]:
        raise HTTPException(status_code=400, detail="Invalid model name")

    # Simulate a successful payment
    payment_successful = True  # This can be set to False to simulate a failed payment

    if payment_successful:
        # Update user's paid models and credits
        functions = session.exec(select(Functions).where(Functions.id == current_user.id)).first()
        if not functions:
            functions = Functions(id=current_user.id)
            session.add(functions)
        if model_name == "model1":
            functions.model1 = True
            cost = 30
        elif model_name == "model2":
            functions.model2 = True
            cost = 60
        elif model_name == "model3":
            functions.model3 = True
            cost = 90

        functions.cost = cost  # Set the cost value explicitly
        current_user.credits += cost

        session.add(functions)
        session.add(current_user)
        session.commit()
        session.refresh(functions)
        session.refresh(current_user)
        return {"message": "Payment successful", "paid_models": {k: v for k, v in functions.__dict__.items() if k in ["model1", "model2", "model3"]}, "credits_added": cost, "total_credits": current_user.credits}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment failed")