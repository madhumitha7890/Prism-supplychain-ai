from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import simulation
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(simulation.router)
