from datetime import datetime, UTC

from fastapi import Request, BackgroundTasks
from .pre_post_up import log_info


async def do_middleware(request: Request, call_next):
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    ip = str(request.client.host)
    path = str(request.base_url)
    method = str(request.method)
    data_to_write = f'''*********
    path - {path}, method - {method}
    time - {now}, ip - {ip}
********
\n'''
    response = await call_next(request)

    response.headers["header_set"] = "in_middleware"
    if response.background:
        response.background.tasks.append(log_info, data_to_write, "log_file.txt")
    else:
        bgt = BackgroundTasks()
        bgt.add_task(log_info, data_to_write, "log_file.txt")
        response.background = bgt
    return response
