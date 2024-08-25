from aiohttp import ClientSession

from services.client import Client


class EventClient(Client):
    
    @classmethod
    async def fetch_events(cls, session: ClientSession | None = None) -> list[dict]:
        response = await Client.fetch(
            "http://line-provider:8000/events", 
            session, 
            "Failed to get events from line-provider: {}"
        )
        return response
    
    @classmethod
    async def fetch_event(cls, event_id: int, session: ClientSession | None = None) -> dict:
        response = await Client.fetch(
            f"http://line-provider:8000/event/{event_id}", 
            session, 
            "Failed to get event from line-provider: {}"
        )
        return response

