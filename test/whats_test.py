import aiohttp
import pytest
from unittest.mock import AsyncMock, patch

from start.whatsapp_quickstart import WhatsAppStart, ACCESS_TOKEN, RECIPIENT_WAID, VERSION, PHONE_NUMBER_ID


@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.mark.asyncio
async def test_send_whatsapp_message_success(mock_session):
    expected_data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_WAID,
        "type": "template",
        "template": {"name": "hello_world", "language": {"code": "en_ES"}},
    }
    expected_response = {"status": "success"}  # Define expected response

    # Mock the _post method to return the expected response
    mock_post = AsyncMock(return_value=expected_response)
    with patch.object(WhatsAppStart, "_post", mock_post):
        response = await WhatsAppStart.send_whatsapp_message(mock_session, RECIPIENT_WAID, "hello_world", "en_ES")

    assert mock_session.post.call_args == (WhatsAppStart.BASE_URL, WhatsAppStart.HEADERS, expected_data)
    assert response == expected_response

@pytest.mark.asyncio
async def test_send_whatsapp_message_failure(mock_session):
    mock_post = AsyncMock(side_effect=aiohttp.ClientResponseError("Request failed", request_info=None)) # type: ignore
    with patch.object(WhatsAppStart, "_post", mock_post):
        with pytest.raises(aiohttp.ClientResponseError):
            await WhatsAppStart.send_whatsapp_message(mock_session, RECIPIENT_WAID, "hello_world", "en_ES")

    mock_session.post.assert_called_once()  # Verify the call was made

@pytest.mark.asyncio
async def test_send_text_message_success(mock_session):
    expected_data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": RECIPIENT_WAID,
        "type": "text",
        "text": {"preview_url": False, "body": "Hello, this is a test message."},
    }
    expected_response = {"status": "success"}  # Define expected response

    mock_post = AsyncMock(return_value=expected_response)
    with patch.object(WhatsAppStart, "_post", mock_post):
        response = await WhatsAppStart.send_text_message(mock_session, RECIPIENT_WAID, "Hello, this is a test message.")

    assert mock_session.post.call_args == (WhatsAppStart.BASE_URL, WhatsAppStart.HEADERS, expected_data)
    assert response == expected_response

@pytest.mark.asyncio
async def test_send_text_message_failure(mock_session):
    mock_post = AsyncMock(side_effect=aiohttp.ClientResponseError("Request failed", request_info=None)) # type: ignore
    with patch.object(WhatsAppStart, "_post", mock_post):
        with pytest.raises(aiohttp.ClientResponseError):
            await WhatsAppStart.send_text_message(mock_session, RECIPIENT_WAID, "Hello, this is a test message.")

    mock_session.post.assert_called_once()  # Verify the call was made

@pytest.mark.asyncio
async def test_send_whatsapp_message_with_invalid_template_name(mock_session):
    with pytest.raises(ValueError):
        await WhatsAppStart.send_whatsapp_message(mock_session, RECIPIENT_WAID, "invalid_template_name", "en_ES")

@pytest.mark.asyncio
async def test_send_whatsapp_message_with_invalid_language_code(mock_session):
    with pytest.raises(ValueError):
        await WhatsAppStart.send_whatsapp_message(mock_session, RECIPIENT_WAID, "hello_world", "invalid_language_code")

@pytest.mark.asyncio
async def test_send_text_message_with_invalid_recipient_type(mock_session):
    with pytest.raises(ValueError):
        await WhatsAppStart.send_text_message(mock_session, RECIPIENT_WAID, "Hello, this is a test message.", recipient_type="invalid_recipient_type") # type: ignore