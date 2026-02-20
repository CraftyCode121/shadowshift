from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.database import Base, engine
from app.auth.routes import router as auth_router
from app.billing.routes import router as billing_router
from app.media.routes import router as media_router 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shadow Shift API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(auth_router)
app.include_router(billing_router)
app.include_router(media_router)  

@app.get("/")
def root():
    return {"message": "API running"}

@app.get("/health")
def health():
    return {"status": "healthy"}