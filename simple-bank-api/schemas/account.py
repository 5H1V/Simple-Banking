from pydantic import BaseModel


class CreateAccountRequest(BaseModel):
    userId: str
    accountType: str


class AmountRequest(BaseModel):
    amount: float