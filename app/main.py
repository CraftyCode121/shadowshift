from fastapi import FastAPI
from app.database import Base, engine
from app.auth.routes import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Media Enhancement API (ShadowShift)",
    version="1.0.0",
    description="Video and photo enhancement service"
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "API is up and running"}

@app.get("/health")
def health():
    return {"status": "healthy"}