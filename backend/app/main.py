from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routers import airplane, flight, hangar, passenger

app = FastAPI(title="Airplanes Manager API", version="0.1.0")

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hangar.router)
app.include_router(airplane.router)
app.include_router(flight.router)
app.include_router(passenger.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
