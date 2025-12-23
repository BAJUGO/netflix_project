from datetime import datetime, UTC

from fastapi import FastAPI, middleware, Request, BackgroundTasks


def log_info(data_to_write):
    with open("D:\project_db_auth\project_dir\loging\lof_file.txt", "a") as file:
        file.write(data_to_write)



async def do_middleware(request: Request, call_next):
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    ip = str(request.client.host)
    path = str(request.base_url)
    method = str(request.method)
    data_to_write= f'''*********
    path - {path}, method - {method}
    time - {now}, ip - {ip}
********
\n'''
    response = await call_next(request)

    response.headers["cool_header"] = "cool_header"
    if response.background:
        response.background.tasks.append(log_info, data_to_write)
    else:
        bgt = BackgroundTasks()
        bgt.add_task(log_info, data_to_write)
        response.background = bgt
    return response