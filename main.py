"""
main.py

This module is the entry point for the FastAPI application. It is responsible for:
1. Loading environment variables
2. Initializing the FastAPI application instance
3. Configuring logging
4. Establishing a connection to MongoDB
5. Configuring middleware
6. Registering route handlers
7. Running the application (when this module is run directly)

Author:
    Yi-Ting Li (yitingli.public@gmail.com)

Usage:
    Run this script directly to start the FastAPI application:
    $ python main.py
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from database.mongodb import MongoDBConnector
from middlewares.cors_middleware import add_middleware
from routes.multimedia import router as multimedia_router
from utils.logger import init_logging

# Load environment variables
# The file name is determined based on the ENV environment variable
env_fname = f".env.{os.getenv('ENV')}" if os.getenv("ENV") else ".env"
load_dotenv(env_fname)

# Initialize FastAPI application
# The debug mode and title are set based on environment variables
app = FastAPI(
    debug=True if os.getenv("ENV") == "dev" else False,
    title=os.getenv("APP_NAME"),
)

# Initialize logger
init_logging()

# Initialize MongoDB connection
# The MongoDBConnector is initialized with the FastAPI application instance
# and is then used to establish a connection to MongoDB
mongodb_connector = MongoDBConnector(app=app)
mongodb_connector.connect_to_mongo()

# Add middlewares
# The add_middleware function is imported from middlewares.cors_middleware
# and is used to configure middleware for the FastAPI application
add_middleware(app)

# Add routes
# Route handlers are registered with the FastAPI application instance
# using the include_router method
app.include_router(multimedia_router, prefix="/multimedia", tags=["multimedia"])

# This block checks if this script is run directly and not imported as a module
# If run directly, it will use Uvicorn to run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("ENV") == "dev" else False,
    )
