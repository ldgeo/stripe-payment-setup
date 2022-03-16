import stripe

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import EmailStr, constr

from stripe_setup_payment.settings import Settings

config = Settings()
app = FastAPI(description="Setup new payments methods for customers")

stripe.api_key = config.STRIPE_API_KEY


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse("/docs")


@app.get("/success", include_in_schema=False)
def success():
    return "Payment method registered ✨"


@app.get("/cancel", include_in_schema=False)
def cancel():
    return "Operation canceled 🚫"


def session_url(customer_id: str) -> str:
    """
    https://stripe.com/docs/payments/sepa-debit/set-up-payment?platform=checkout
    """
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=config.PAYMENT_METHOD_TYPES,
        mode="setup",
        customer=customer_id,
        success_url=config.HOST + "/success",
        cancel_url=config.HOST + "/cancel",
    )
    return checkout_session.url


@app.get("/email/{email}", summary="Setup a new payment method by email")
def setup_new_method_by_email(email: EmailStr):
    customer = stripe.Customer.list(email=email)

    if not customer:
        raise HTTPException(
            status_code=404, detail=f"No customer with this email: {email}"
        )

    if len(customer.data) > 1:
        raise HTTPException(
            status_code=404,
            detail="Several users with this email, please use /setup/{customer_id} instead",
        )

    return RedirectResponse(session_url(customer.data[0].id), status_code=303)


@app.get("/id/{customer_id}", summary="Setup a new payment method by user id")
def setup_new_method_by_id(customer_id: constr(regex=r"cus_.*")):
    try:
        customer = stripe.Customer.retrieve(customer_id)
    except stripe.error.InvalidRequestError as exc:
        raise HTTPException(status_code=404, detail=exc.error.message)

    return RedirectResponse(session_url(customer.id), status_code=303)


def serve():
    uvicorn.run(app, host=config.HOST.host, port=int(config.HOST.port))
