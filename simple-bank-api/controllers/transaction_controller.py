from fastapi import APIRouter

transaction_controller = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)