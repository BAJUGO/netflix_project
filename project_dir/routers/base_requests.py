from fastapi import APIRouter, Response, Depends
from project_dir import authorization as auth


router = APIRouter()


@router.get("/initPage", dependencies=[Depends(auth.get_current_user_access_token)])
async def check_the_data():
    return Response(status_code=200, content="OK")