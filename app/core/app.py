from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from api.router import api_router
from core.di.container import Container


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="Sidus",
        description="Test task for Sidus Project",
        version="1.0",
        docs_url="/api/docs/",
        redoc_url="/api/redoc/",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    container = Container()
    app.state.container = container

    app.include_router(router=api_router, prefix="/api")

    return app
