import asyncio
import logging

import aiohttp

from app import create_app

from start import whatsapp_quickstart as whapp


app = create_app()

@app.route('/send_message') # type: ignore
def send_message_route():
    # recipient = whapp.RECIPIENT_WAID
    # text = "Hello, this is a test message."
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(whapp.send_text_message(aiohttp.ClientSession(), recipient, text))
    # return "Message sent"
    asyncio.run(whapp.send_text_message(aiohttp.ClientSession(), whapp.RECIPIENT_WAID, "Hello, this is a test message.")) # type: ignore


if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=8000)
