from fastapi import Header
from fastapi import HTTPException
from fastapi import status


API_KEY = "BHASHABRIDGE_SECRET_KEY"


async def verify_api_key(

    x_api_key: str = Header(default=None)

):

    if x_api_key != API_KEY:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )