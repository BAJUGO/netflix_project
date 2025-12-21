from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from project_dir.authorization.token_enc_dec import decode_access_token
from project_dir.authorization.token_schemas import AccessTokenData

oauth2_schema = OAuth2PasswordBearer(tokenUrl="create_token")


def get_current_user_access_token(token: str = Depends(oauth2_schema)) -> AccessTokenData:
    return AccessTokenData(**decode_access_token(token))



def get_user_with_role(required_role:str):
    def subfunction_required_role(user_token: AccessTokenData = Depends(get_current_user_access_token)):
        if user_token.role != required_role:
            raise HTTPException(status_code=403, detail="Not enough rights")
        return user_token
    return subfunction_required_role