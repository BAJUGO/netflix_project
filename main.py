from fastapi import FastAPI
from project_dir.views_part import routers_router
app = FastAPI()

app.include_router(routers_router)

#! НЕ ЗАБУДЬ ПЕРЕНЕСТИ MAIN В PROJECT DIR. ЗАПУСК ДЕЛАТЬ ЧЕРЕЗ UVICORN.RUN