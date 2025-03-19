import aiohttp

from app.config import PassportConfig
from app.cores.errors import ForbiddenException
from app.dto.passport import PassportResponse


class Passport:
    def __init__(self, config: PassportConfig):
        self.config = config

    async def authenticate(self, token: str):
        headers = {"cookie": f"token={token}"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                self.config.uri,
            ) as resp:
                resp.raise_for_status()
                parsed = await resp.json()
                passport_response = PassportResponse(**parsed)
                if passport_response.data.is_blocked:
                    raise ForbiddenException("User is blocked")
                return passport_response
