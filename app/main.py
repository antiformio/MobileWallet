import uvicorn

from fastapi_sqlalchemy import DBSessionMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware
from app.api import users, wallets, transactions, auth


import os

load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(wallets.router)
app.include_router(transactions.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
