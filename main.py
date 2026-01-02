from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from project_dir.authorization import authorization_router
from project_dir.loging_and_exc import lifespan_loging, do_middleware, custom_exception_handler
from project_dir.views_part import routers_router

app = FastAPI(lifespan=lifespan_loging)

app.include_router(routers_router)
app.include_router(authorization_router)
app.middleware("http")(do_middleware)

custom_exception_handler(app)


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs#")

# ! НЕ ЗАБУДЬ ПЕРЕНЕСТИ MAIN В PROJECT DIR. ЗАПУСК ДЕЛАТЬ ЧЕРЕЗ UVICORN.rUN
