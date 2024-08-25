from fastapi import HTTPException

from aiohttp import ClientSession


class Client:
    
    @classmethod
    async def fetch(
            cls, 
            url: str, 
            session: ClientSession | None = None, 
            exception_detail: str | None = None
    ) -> list[dict] | dict:
        session_create = False
        if session is None:
            session = ClientSession()   
            session_create = True
            
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=500,
                    detail=exception_detail.format(await response.text()) if exception_detail else await response.text(),
                )
            response = await response.json()

        if session_create:
            await session.close()

        return response
