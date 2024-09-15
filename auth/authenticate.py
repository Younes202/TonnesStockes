from auth.jwt_handler import verify_access_token
from fastapi import HTTPException, status, Request


async def authenticate(request: Request) -> str:
    session_id = request.session.get('session_id')
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign in for access"
        )
    decode_token = verify_access_token(session_id)
    return decode_token["user"]
