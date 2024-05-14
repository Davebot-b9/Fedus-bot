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

class WhatsAppStart:
    BASE_URL = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    HEADERS = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    @staticmethod
    async def send_whatsapp_message(session, recipient, template_name, language_code):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "template",
            "template": {"name": template_name, "language": {"code": language_code}},
        }
        return await WhatsAppStart._post(session, data)

    @staticmethod
    async def send_text_message(session, recipient, text):
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
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