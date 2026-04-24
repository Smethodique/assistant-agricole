from fastapi import FastAPI
from backend.routes import predict, chat, simulate

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Precision Farming Assistant API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Precision Farming Assistant API"}

app.include_router(predict.router, prefix="/predict", tags=["prediction"])
app.include_router(simulate.router, prefix="/simulate", tags=["simulation"])
