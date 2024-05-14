import pytest
from start.whatsapp_quickstart import WhatsAppStart

class MockSession:
    async def post(self, url: str, headers: dict, json: dict):
        return MockResponse()

class MockResponse:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def json(self):
        return {"status": "success"}

@pytest.mark.asyncio
async def test_send_whatsapp_message():
    session = MockSession()
    response = await WhatsAppStart.send_whatsapp_message(
        session, 
        "1234567890", 
        "hello_world", 
        "en_ES"
    )
    assert response == {"status": "success"}

@pytest.mark.asyncio
async def test_send_text_message():
    session = MockSession()
    response = await WhatsAppStart.send_text_message(
        session, 
        "1234567890", 
        "Hello, this is a test message."
    )
    assert response == {"status": "success"}