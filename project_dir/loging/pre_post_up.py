from contextlib import asynccontextmanager
from datetime import datetime, UTC
from fastapi import FastAPI



def log_info(data):
    with open("D:/project_db_auth/project_dir/loging/lof_file.txt", "a") as file:
        file.write(data)


@asynccontextmanager
async def lifespan_loging(app: FastAPI):
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    log_info(f'''{"*" * 30}
app word started now - {now}
\n\n\n\n''')
    yield
    log_info(f'''app work ended now - {now}
{"*" * 30}\n\n\n\n''')


