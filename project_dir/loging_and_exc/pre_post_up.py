from contextlib import asynccontextmanager
from datetime import datetime, UTC
from fastapi import FastAPI



def log_info(data, where_to_load: str):
    with open(f"D:/project_db_auth/project_dir/loging_and_exc/{where_to_load}", "a") as file:
        file.write(data)


@asynccontextmanager
async def lifespan_loging(app: FastAPI):
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    log_info(f''' \n\n{"*" * 30}
app word started now - {now}
\n\n\n\n''', "log_file.txt")
    yield
    log_info(f'''app work ended now - {now}
{"*" * 30}\n\n\n\n''', "log_file.txt")


