from fastapi import FastAPI
from app.database import Base, engine
from app.auth.routes import router as auth_router
from app.billing.routes import router as billing_router  

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Media Enhancement API")

app.include_router(auth_router)
app.include_router(billing_router)  

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}