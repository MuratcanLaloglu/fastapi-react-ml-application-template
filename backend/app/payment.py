from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from .models import User
from .auth import get_current_user
from .dependencies import get_session

router = APIRouter()

@router.post("/payment")
async def process_payment(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    # Simulate a successful payment
    payment_successful = True  # This can be set to False to simulate a failed payment

    if payment_successful:
        # Update user credits
        current_user.credits += 30
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return {"message": "Payment successful", "credits_added": 30, "total_credits": current_user.credits}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment failed")