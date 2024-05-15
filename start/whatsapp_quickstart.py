import json
import os
import asyncio
from dotenv import load_dotenv
import aiohttp

# Load environment variables
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

# Define valid template names and language codes
VALID_TEMPLATE_NAMES = ["hello_world", "reminder"]
VALID_LANGUAGE_CODES = ["en_ES", "es_ES"]

# Define valid recipient types
VALID_RECIPIENT_TYPES = ["individual", "group"]

class WhatsAppStart:
    BASE_URL = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    HEADERS = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    @staticmethod
    async def send_whatsapp_message(session, recipient, template_name, language_code):
        """
        Sends a WhatsApp message using a template.

        Args:
        session: An aiohttp.ClientSession object.
        recipient_waid: The WhatsApp ID of the recipient.
        template_name: The name of the template to use.
        language_code: The language code of the template.

        Returns:
        A dictionary containing the response from the WhatsApp API.
        """

        # Validate the input parameters
        if template_name not in VALID_TEMPLATE_NAMES:
            raise ValueError(f"Invalid template name: {template_name}")
        if language_code not in VALID_LANGUAGE_CODES:
            raise ValueError(f"Invalid language code: {language_code}")

        data = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "template",
            "template": {"name": template_name, "language": {"code": language_code}},
        }
        return await WhatsAppStart._post(session, data)

    @staticmethod
    async def send_text_message(session, recipient, text, recipient_type: str = "individual"):
        """
        Sends a WhatsApp text message.

        Args:
        session: An aiohttp.ClientSession object.
        recipient_waid: The WhatsApp ID of the recipient.
        message: The message to send.
        recipient_type: The type of recipient (individual or group).

        Returns:
        A dictionary containing the response from the WhatsApp API.
        """

        # Validate the input parameters
        if recipient_type not in VALID_RECIPIENT_TYPES:
            raise ValueError(f"Invalid recipient type: {recipient_type}")

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
        return await WhatsAppStart._post(session, data)

    @staticmethod
    async def _post(session, data):
        async with session.post(WhatsAppStart.BASE_URL, headers=WhatsAppStart.HEADERS, json=data) as response:
            return await response.json()

# Main function (commented out)
# async def main():
#     async with aiohttp.ClientSession() as session:
#         response = await WhatsAppStart.send_whatsapp_message(session, RECIPIENT_WAID, "hello_world", "en_ES")
#         print(response)
#         response = await WhatsAppStart.send_text_message(session, RECIPIENT_WAID, "Hello, this is a test message.")
#         print(response)

# Run the main function (commented out)
# asyncio.run(main())