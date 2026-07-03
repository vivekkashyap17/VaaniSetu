from fastapi import Header
from fastapi import HTTPException
from fastapi import status


from app.core.config.settings import get_settings

settings = get_settings()

async def verify_api_key(

    x_api_key: str = Header(default=None)

):

    if x_api_key != settings.API_KEY:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )