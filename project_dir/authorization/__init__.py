__all__ = (
    "authorization_router",
    "oauth2_schema",

)
from .auth_router import router as authorization_router
from .auth_deps import oauth2_schema