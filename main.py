from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from project_dir.loging_and_exc import lifespan, do_middleware, custom_exception_handler
from project_dir.routers import get_post_router, del_put_patch_router


app = FastAPI(lifespan=lifespan)
app.middleware("http")(do_middleware)
app.include_router(get_post_router)
app.include_router(del_put_patch_router)



custom_exception_handler(app)

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs#")

# ! НЕ ЗАБУДЬ ПЕРЕНЕСТИ MAIN В PROJECT DIR. ЗАПУСК ДЕЛАТЬ ЧЕРЕЗ UVICORN.rUN
