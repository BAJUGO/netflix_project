__all__ = ("get_post_router", "del_put_patch_router", "base_requests_router")

from .get_post_router import router as get_post_router
from .delete_put_patch_router import router as del_put_patch_router
from .base_requests import router as base_requests_router