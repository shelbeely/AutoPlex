from fastapi import FastAPI
from src.api.routes import media, query, recommendations
from src.utils.logging import get_logger

# Initialize FastAPI application
app = FastAPI(
    title="AutoPlex Media Management API",
    description="Intelligent media management system integrating Plex metadata with LLM-powered recommendations",
    version="1.0.0"
)

# Get logger
log = get_logger(__name__)

# Include API routers
app.include_router(media.router)
app.include_router(query.router)
app.include_router(recommendations.router)

# Beginner's Tip: This is the main FastAPI application where we register all our route modules.
# By including routers from different modules, we maintain a clean separation of concerns.

# Fun Fact: FastAPI can handle over 300,000 requests per minute depending on the server setup!
