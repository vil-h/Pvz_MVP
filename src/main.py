from fastapi import FastAPI, APIRouter
from src.routers.orders import router
#uvicorn src.main:app --reload
app = FastAPI()
app.include_router(router)
