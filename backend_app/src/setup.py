from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger(__name__)


def app_init() -> FastAPI:
    logger.info("Initializing Capacity API")

    app = FastAPI(
        title="Capacity API",
        description="Shipping capacity analytics API for corridor-level TEU tracking",
        version="1.0.0",
        debug=False
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from backend_app.src import routes
    if hasattr(routes, 'init_app') and callable(routes.init_app):
        routes.init_app(app)
        logger.info("Routes loaded successfully")
    else:
        logger.warning("routes.py does not have init_app function")

    @app.on_event("startup")
    async def startup_event():
        logger.info("Capacity API started successfully")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Capacity API shutting down")

    return app
