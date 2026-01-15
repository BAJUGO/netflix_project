from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


from project_dir.logging_and_exc import lifespan, do_middleware, custom_exception_handler
from project_dir.routers import *

app = FastAPI(lifespan=lifespan)
app.middleware("http")(do_middleware)
app.include_router(get_post_router)
app.include_router(del_put_patch_router)
app.include_router(base_requests_router)

custom_exception_handler(app)


app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs#")

# ! НЕ ЗАБУДЬ ПЕРЕНЕСТИ MAIN В PROJECT DIR. ЗАПУСК ДЕЛАТЬ ЧЕРЕЗ UVICORN.rUN
