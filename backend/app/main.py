from fastapi import FastAPI
from database import engine
from models import models
from routers import auth, users, hospitals, requests, donations

Base = models.Base  # This should work now

app = FastAPI(title="Blood Donation API")

@app.get('/')
def main():
    return {"data": "The API is doing well"}

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(hospitals.router)
app.include_router(requests.router)
app.include_router(donations.router)