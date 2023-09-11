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

# Load environment variables
# The file name is determined based on the ENV environment variable
env_fname = f".env.{os.getenv('ENV')}" if os.getenv("ENV") else None
if env_fname is not None:
	print(f'using .env file "{env_fname}"')
	load_dotenv(env_fname)
else:
	print(f'using env vars')

from configs import firebase_conf

firebase_conf.init_firebase()


from fastapi import FastAPI

from database.firestore import FirebaseConnector
from database.mongodb import MongoDBConnector
from middlewares.cors_middleware import add_middleware
from routes.chat import router as chat_router
from routes.feedback import router as feedback_router
from routes.user import router as user_router
from utils.logger import init_logging

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
mongodb_connector.connect_to_db()

# Initialize Firebase connection
# The FirebaseConnector is initialized with the FastAPI application instance
# and is then used to establish a connection to Firebase
firebase_connector = FirebaseConnector(app=app)
firebase_connector.connect_to_db()

# Add middlewares
# The add_middleware function is imported from middlewares.cors_middleware
# and is used to configure middleware for the FastAPI application
add_middleware(app)

# Add routes
# Route handlers are registered with the FastAPI application instance
# using the include_router method
# app.include_router(multimedia_router, prefix="/multimedia", tags=["multimedia"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(feedback_router, prefix="/feedback", tags=["feedback"])

# This block checks if this script is run directly and not imported as a module
# If run directly, it will use Uvicorn to run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("APP_PORT")),
        reload=True if os.getenv("ENV") == "dev" else False,
    )
