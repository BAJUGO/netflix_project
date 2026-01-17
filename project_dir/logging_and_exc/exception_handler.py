from datetime import datetime, UTC

from fastapi import FastAPI, Request, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError
from sqlalchemy.exc import IntegrityError

from .pre_post_up import log_info


# TODO Сделать эту функцию
def exception_request_worker(request: Request):
    pass


def custom_exception_handler(app: FastAPI):
    @app.exception_handler(IntegrityError)
    async def work_with_unique_db(request: Request, exc: IntegrityError):
        msg = str(exc.orig)
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        ip = str(request.client.host)
        path = str(request.base_url)
        detail = "None"
        if "users_visible_name_key" in msg:
            detail = "Such username has been already taken! Try other one!"
        elif "users_email_key" in msg:
            detail = (
                "Such email was already registered! Either login or write other email"
            )
        # log_info(
        #     data=f"Integrity exception: {detail}\nTime: {now} - Ip: {ip}\nPath: {path}\n\n",
        #     where_to_load="exceptions_log.txt",
        # )
        return JSONResponse(status_code=401, content={"detail": detail})

    @app.exception_handler(HTTPException)
    async def work_with_http_exception(request: Request, exc: HTTPException):
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        ip = str(request.client.host)
        path = str(request.base_url)
        method = str(request.method)
        # log_info(
        #     data=f"HTTPException: {exc.detail}. s_code: {exc.status_code}\nTime: {now} - Ip: {ip}\nPath: {path} + method: {method}\n\n",
        #     where_to_load="exceptions_log.txt",
        # )
        return await http_exception_handler(request, exc)

    @app.exception_handler(ExpiredSignatureError)
    async def work_with_expire_signature(request: Request, exc: ExpiredSignatureError):
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        ip = str(request.client.host)
        path = str(request.base_url)
        method = str(request.method)
        # log_info(
        #     data=f"Expired Signature Error. \nTime: {now} - Ip: {ip}\nPath: {path} + method: {method}\n\n",
        #     where_to_load="exceptions_log.txt",
        # )
        return JSONResponse(
            status_code=401, content={"detail": "your token is expired. Relogin"}
        )
