from contextlib import asynccontextmanager
from datetime import datetime, UTC
from fastapi import FastAPI, Request



def log_info(data, where_to_load: str):
    with open(f"D:/project_db_auth/project_dir/loging_and_exc/{where_to_load}", "a") as file:
        file.write(data)


@asynccontextmanager
async def lifespan_loging(app: FastAPI):
    log_info(
        data="\n$$$$$  application has been started\n", where_to_load="log_file.txt"
    )
    yield
    log_info(
        data="\n$$$$$  application has been stopped\n", where_to_load="log_file.txt"
    )

