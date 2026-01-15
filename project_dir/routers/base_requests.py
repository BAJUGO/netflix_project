from fastapi import APIRouter, Response, Depends, Request
from project_dir import authorization as auth


router = APIRouter()


@router.get("/initPage")
async def check_the_data(token=Depends(auth.get_current_user_access_token)):
    if token :
        return Response(status_code=200, content="OK")
    return Response(status_code=401, content='')


@router.get("/deleteCookies")
async def delete_cookies(req: Request, resp: Response):
    if req.cookies.get("access_token") and req.cookies.get("refresh_token"):
        resp.delete_cookie(key="access_token", path="/")
        resp.delete_cookie(key="refresh_token", path="/")
        resp.status_code, resp.content = 200, "ok"
        return resp
    resp.status_code, resp.content = 401, ''
    return resp