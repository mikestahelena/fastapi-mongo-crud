import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from app.customer.routers import router as customer_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown():
    app.mongodb_client.close()


app.include_router(router=customer_router, prefix="/customer")

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
