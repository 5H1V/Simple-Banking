from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router

app = FastAPI(
    title="Simple Bank API",
    description="REST API for the Simple Bank Application",
    version="1.0.0"
)

# Solves issues of having application run on 2 different ports (frontend, backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    # uvicorn runs FastAPI application
    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=5000,
        reload=True
    )