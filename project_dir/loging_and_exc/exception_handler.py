from fastapi import FastAPI, Request
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from .pre_post_up import log_info
from datetime import datetime, UTC




def custom_exception_handler(app: FastAPI):
    @app.exception_handler(IntegrityError)
    async def work_with_unique_db(request: Request, exc: IntegrityError):
        msg = str(exc.orig)
        detail = "None"
        if "users_visible_name_key" in msg:
            detail = "Such username has been already taken! Try other one!"
            log_info(f"Such_visible_name_exist_error\nclient - {request.client}\n{datetime.now(UTC)}\n\n", "exceptions_log.txt")
        elif "users_email_key" in msg:
            detail = "Such email was already registered! Either login or write other email"
            log_info(f"Such_email_already_exist_error\nclient - {request.client}\n{datetime.now(UTC)}\n\n", "exceptions_log.txt")
        return JSONResponse(status_code=401, content={"detail": detail})
