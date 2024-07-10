from fastapi import FastAPI
import uvicorn

from application.api.users import handlers as users_router
from application.api.categories import handlers as categories_handlers
from application.api.tasks import handlers as tasks_handlers
from application.api.app import handlers as app_handlers
from logic import init_container
from configs.config import ConfigSettings


def start_app() -> FastAPI:
    app = FastAPI(
        title="todo",
        description="todo API",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )
    app.include_router(users_router.router)
    app.include_router(categories_handlers.router)
    app.include_router(tasks_handlers.router)
    app.include_router(app_handlers.router)
    return app


if __name__ == "__main__":
    uvicorn.run(start_app(), host="localhost", port=init_container().resolve(ConfigSettings).api_port)
