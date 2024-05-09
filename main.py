from fastapi import FastAPI
from app.routers import vendor_urls
app = FastAPI()

app.include_router(router=vendor_urls.router)