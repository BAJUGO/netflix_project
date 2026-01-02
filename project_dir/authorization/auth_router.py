from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from project_dir.authorization.auth_deps import get_current_user_access_token, admin_dep
from project_dir.authorization.token_enc_dec import encode_access_token, encode_refresh_token
from project_dir.authorization.token_schemas import AccessTokenData
from project_dir.authorization.utilites import authenticate_user
from project_dir.core import ses_dep
from project_dir.views_part.crud import add_user_session, delete_user_session, change_role_session
from project_dir.views_part.schemas import UserCreate

router = APIRouter()


# create token


@router.post("/create_token", tags=["token"])
async def check_function(user=Depends(authenticate_user)):
    data_for_token = {"sub": str(user.id), "name": user.visible_name, "role": user.role, "id": user.id}
    access_token = encode_access_token(data=data_for_token)
    refresh_token = encode_refresh_token(data=data_for_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/for_users_only", tags=["token"])
async def return_user_token_info(user_token: AccessTokenData = Depends(get_current_user_access_token)):
    return f"Hello {user_token.name}! Your role is {user_token.role} Your id is {user_token.id}"


@router.get("/for_admins_only", tags=["token"])
async def return_admin_token_info(user_token: AccessTokenData = admin_dep):
    return f"Hello admin! Your name is {user_token.name}"


@router.post("/register", tags=["user", "add"])
async def add_new_user(user_in: UserCreate, session: AsyncSession = ses_dep):
    return await add_user_session(user_in, session)


@router.delete("/delete_account", tags=["user", "delete"], dependencies=[admin_dep])
async def delete_user(user_id: int, session: AsyncSession = ses_dep):
    return await delete_user_session(user_to_delete_id=user_id, session=session)


@router.patch("/role_setter/{user_id}", tags=["user", "update"], dependencies=[admin_dep])
async def change_user_role(user_id: int, role_to_change: str = Form(...),
                           session: AsyncSession = ses_dep):
    return await change_role_session(session, user_id, role_to_change)
