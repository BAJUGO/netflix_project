from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from backend.authorization.token_schemas import AccessTokenData
from backend.authorization.token_enc_dec import get_token_from_cookies
from backend.logging_and_exc import log_info

oauth2_schema = OAuth2PasswordBearer(tokenUrl="create_token")


def get_current_user_access_token(
        request: Request
) -> AccessTokenData | None:
    try:
        token = get_token_from_cookies(request=request, token_type="access_token")
        return AccessTokenData(**token)
    except Exception as e:
        #log_info(data=f"{str(e)} \n", where_to_load="../logging_and_exc/exceptions_log.txt")
        pass


def get_user_with_role(required_role: list[str]):
    def subfunction_required_role(
            user_token: AccessTokenData = Depends(get_current_user_access_token),
    ) -> AccessTokenData:
        if user_token.role not in required_role:
            raise HTTPException(status_code=403, detail="Not enough rights")
        return user_token

    return subfunction_required_role


admin_dep = Depends(get_user_with_role(["admin"]))
admin_or_mod_dep = Depends(get_user_with_role(["admin", "moderator"]))
