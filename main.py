import uvicorn
import sys
import logging
from dotenv import load_dotenv  # Import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from users.route import user_router
from categories.route import category_router
from database.connection import Settings, get_database
from auth.authenticate import authenticate

import os
# Load environment variables from .env file
load_dotenv(".env")

# Print out loaded environment variables for debugging
print(os.getenv("DATABASE_URL"))
print(os.getenv("SECRET_KEY"))

logger = logging.getLogger(__name__)
# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/node_modules", StaticFiles(directory="node_modules"),
          name="static")

# Initialize the database on startup
settings = Settings()


async def startup_event():
    try:
        await settings.initialize_database()
    except Exception as e:
        logger.exception(f"Exception during startup: {e}")
        sys.exit(1)


app.add_event_handler("startup", startup_event)

# Add cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods="*",  # Allow only get and post methods
    allow_headers=["*"],
)

# Add SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=os.environ["SECRET_KEY"])
# Include routers via include router from APIRouter
app.include_router(
    user_router,
    prefix="/user",
)



app.include_router(
    category_router,
    prefix="/category",
)



# Serve the main component of the Vue.js app
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

if __name__ == '__main__':
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8001)
    except KeyboardInterrupt:
        # Handle the KeyboardInterrupt, perform cleanup, and exit gracefully
        logger.info("KeyboardInterrupt received. Cleaning up...")
        # Add cleanup code as needed
        sys.exit(0)