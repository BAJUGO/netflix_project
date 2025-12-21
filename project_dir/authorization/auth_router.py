from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project_dir.authorization.auth_deps import get_current_user_access_token, get_user_with_role
from project_dir.authorization.token_enc_dec import encode_access_token
from project_dir.authorization.token_schemas import AccessTokenData
from project_dir.authorization.utilites import authenticate_user
from project_dir.core import db_helper
from project_dir.views_part.crud import add_user_session
from project_dir.views_part.schemas import UserCreate, UserSchema

router = APIRouter(tags=["token"])


# create token


@router.post("/create_token")
async def check_function(user=Depends(authenticate_user)):
    data_for_token = {"name": user.visible_name, "role": user.role, "id": user.id}
    access_token = encode_access_token(data=data_for_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/for_users_only")
async def return_user_token_info(user_token: AccessTokenData = Depends(get_current_user_access_token)):
    return f"Hello {user_token.name}! Your role is {user_token.role} Your id is {user_token.id}"


@router.get("/for_admins_only")
async def return_admin_token_info(user_token: AccessTokenData = Depends(get_user_with_role("admin"))):
    return f"Hello admin! Your name is {user_token.name}"


@router.post("/register")
async def add_new_user(user_in: UserCreate, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await add_user_session(user_in, session)