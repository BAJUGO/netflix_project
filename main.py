from fastapi import FastAPI, Depends, Response
from fastapi.responses import RedirectResponse

from project_dir import authorization as auth
from project_dir.logging_and_exc import lifespan, do_middleware, custom_exception_handler
from project_dir.routers import get_post_router, del_put_patch_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(lifespan=lifespan)
app.middleware("http")(do_middleware)
app.include_router(get_post_router)
app.include_router(del_put_patch_router)

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


@app.get("/initPage")
async def check_the_data(token=Depends(auth.get_current_user_access_token)):
    return Response(status_code=200, content="OK")

# ! НЕ ЗАБУДЬ ПЕРЕНЕСТИ MAIN В PROJECT DIR. ЗАПУСК ДЕЛАТЬ ЧЕРЕЗ UVICORN.rUN
