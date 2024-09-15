from database.connection import Database
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from auth.authenticate import authenticate
from fastapi import APIRouter, HTTPException, status, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
import logging
from .model import User, TokenResponse

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")
user_router = APIRouter(
    tags=["User"],
)

user_database = Database(User)
hash_password = HashPassword()


@user_router.post("/signup")
async def sign_user_up(email: str = Form(...), password: str = Form(...)):
    try:
        # Check if user already exists
        user_exist = await User.find_one(User.email == email)
        if user_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists."
            )

        # Hash password and save user
        hashed_password = hash_password.create_hash(password)
        new_user = User(email=email, password=hashed_password)
        await user_database.save(new_user)
        return {"message": "User created successfully"}
    except Exception as e:
        logger.error(f"Error in sign-up: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


# Sign in route
@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(
    request: Request,
    user: OAuth2PasswordRequestForm = Depends()
):
    try:
        # Check if user exists based on the provided email
        user_exist = await User.find_one(User.email == user.username)

        if not user_exist:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "User not found."}
            )

        # Verify the password
        if hash_password.verify_hash(user.password, user_exist.password):
            # Create the access token
            access_token = create_access_token(user_exist.email)

            # Set the session ID in the request session
            request.session['session_id'] = access_token

            # Redirect to the dashboard
            return RedirectResponse(url="/user", status_code=status.HTTP_302_FOUND)
        # If password is incorrect
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid password."}
        )

    except Exception as e:
        # Log the unexpected error for debugging
        logger.error(f"Unexpected error during sign-in: {e}")

        # Return an internal server error response
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )


@user_router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, user: str = Depends(authenticate)):
    # Render the "categories.html" template
    total_categories = 4
    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request, "total_categories": total_categories})


@user_router.get("/log_out", response_class=HTMLResponse)
async def log_out(request: Request, user: str = Depends(authenticate)):
    # Render the "categories.html" template
    return templates.TemplateResponse("errors/unauthorized.html", {"request": request})

