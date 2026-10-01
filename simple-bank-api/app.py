from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.user_controller import user_controller
from controllers.account_controller import account_controller
from controllers.transaction_controller import transaction_controller

app = FastAPI(
    title="Simple Bank API",
    description="REST API for the Simple Bank Application",
    version="1.0.0"
)

# Solves issues of having application run on 2 different ports (frontend, backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adds extenion to route to correct page
app.include_router(user_controller, prefix="/api")

app.include_router(account_controller, prefix="/api")

app.include_router(transaction_controller, prefix="/api")

if __name__ == "__main__":
    # uvicorn runs FastAPI application
    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=5000,
        reload=True
    )