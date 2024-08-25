import pytest

from unittest.mock import Mock, patch
from fastapi import HTTPException
from services.client import Client
from repositories.event_client import EventClient


@pytest.mark.asyncio
async def test_fetch_events_success():
    with patch.object(Client, 'fetch', return_value=Mock()) as mock_fetch:
        response = await EventClient.fetch_events()
        assert mock_fetch.called_once_with(
            "http://line-provider:8000/events", 
            None, 
            "Failed to get events from line-provider: {}"
        )
        assert response == mock_fetch.return_value


@pytest.mark.asyncio
async def test_fetch_events_failure():
    with patch.object(Client, 'fetch', side_effect=HTTPException(status_code=500, detail="Test")) as mock_fetch:
        with pytest.raises(HTTPException):
            await EventClient.fetch_events()
        assert mock_fetch.called_once_with(
            "http://line-provider:8000/events", 
            None, 
            "Failed to get events from line-provider: {}"
        )
        assert mock_fetch.side_effect.detail == "Test"


@pytest.mark.asyncio
async def test_fetch_event_success():
    with patch.object(Client, 'fetch', return_value=Mock()) as mock_fetch:
        response = await EventClient.fetch_event(1)
        assert mock_fetch.called_once_with(
            "http://line-provider:8000/event/1", 
            None, 
            "Failed to get event from line-provider: {}"
        )
        assert response == mock_fetch.return_value


@pytest.mark.asyncio
async def test_fetch_event_failure():
    with patch.object(Client, 'fetch', side_effect=HTTPException(status_code=500, detail="Test")) as mock_fetch:
        with pytest.raises(HTTPException):
            await EventClient.fetch_event(1)
        assert mock_fetch.called_once_with(
            "http://line-provider:8000/event/1", 
            None, 
            "Failed to get event from line-provider: {}"
        )
        assert mock_fetch.side_effect.detail == "Test"
