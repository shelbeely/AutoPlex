"""
AutoPlex Media Management API Entry Point

This file serves as the entry point for running the FastAPI application.
"""

import uvicorn
from src.api import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config="logging.yaml"
    )

# Beginner's Tip: This is the main entry point for our FastAPI application.
# It uses Uvicorn to serve the app with hot-reloading enabled for development.

# Fun Fact: The first web server was created by Tim Berners-Lee in 1990 and was called CERN httpd!
