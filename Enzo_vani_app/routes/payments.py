from fastapi import APIRouter, HTTPException, Request
import stripe
from pydantic import BaseModel
from database import orders_collection
from datetime import datetime
import os

router = APIRouter()

stripe.api_key = "sk_test_xxx" 
endpoint_secret = "whsec_xxx"

class CheckoutRequest(BaseModel):
    items: list  # [{ name, price, quantity }]

@router.post("/create-checkout-session")
def create_checkout_session(checkout_request: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {"name": item["name"]},
                        "unit_amount": int(item["price"] * 100),
                    },
                    "quantity": item["quantity"],
                }
                for item in checkout_request.items
            ],
            mode="payment",
            success_url="http://localhost:5173/success",
            cancel_url="http://localhost:5173/cancel",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Payload inválido
        raise HTTPException(status_code=400, detail=str(e))
    except stripe.error.SignatureVerificationError as e:
        # Firma inválida
        raise HTTPException(status_code=400, detail=str(e))

    # Procesar el evento
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        handle_checkout_completed(session)

    return {"status": "success"}

def handle_checkout_completed(session):
    # Extraemos datos del session
    email = session["customer_email"]
    items = session["display_items"] if "display_items" in session else []
    total = session["amount_total"] / 100  # convertir a euros/dólares

    # Guardamos en Mongo
    orders_collection.insert_one({
        "user_email": email,
        "items": items,
        "total_amount": total,
        "status": "paid",
        "created_at": datetime.utcnow()
    })