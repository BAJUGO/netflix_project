from fastapi import FastAPI

from project_dir.loging.mdlwr import do_middleware
from project_dir.loging.pre_post_up import lifespan_loging
from project_dir.views_part import routers_router
from project_dir.authorization import authorization_router
app = FastAPI(lifespan=lifespan_loging)

app.include_router(routers_router)
app.include_router(authorization_router)
app.middleware("http")(do_middleware)


#! НЕ ЗАБУДЬ ПЕРЕНЕСТИ MAIN В PROJECT DIR. ЗАПУСК ДЕЛАТЬ ЧЕРЕЗ UVICORN.RUN