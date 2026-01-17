from fastapi import APIRouter, Response, Depends, Request
from project_dir import authorization as auth
from project_dir.logging_and_exc import log_info

router = APIRouter()


@router.get("/initPage")
async def check_the_data(request: Request, response: Response, token=Depends(auth.get_current_user_access_token)):
    if token:
        return Response(status_code=200, content="OK")
    else:
        try:
            refresh_token = auth.get_token_from_cookies(token_type="refresh_token", request=request)
            auth.set_new_tokens(data=refresh_token, response=response)
            response.status_code = 200
            return response
        except Exception as e:
            log_info(data=f"{str(e)} \n", where_to_load="../logging_and_exc/exceptions_log.txt")
            response.status_code = 401
            return response



@router.get("/deleteCookies")
async def delete_cookies(request: Request, response: Response):
    if request.cookies.get("access_token") or request.cookies.get("refresh_token"):
        try:
            response.delete_cookie(key="access_token", path="/")
            response.delete_cookie(key="refresh_token", path="/")
        except Exception as e:
            log_info(data=f"{str(e)} \n", where_to_load="../logging_and_exc/exceptions_log.txt")
        response.status_code, response.content = 200, "ok"
        return response
    response.status_code = 401
    return response

