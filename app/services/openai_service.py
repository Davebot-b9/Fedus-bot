import os
import shelve
import asyncio
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

client = OpenAI(api_key=OPENAI_API_KEY)

async def upload_file(path):
    """Upload a file with an 'assistants' purpose"""
    file = await client.files.create(file=open(path, "rb"), purpose="assistants") # type: ignore
    return file

async def create_assistant(file):
    """Create an assistant"""
    assistant = await client.beta.assistants.create(
        name="Fedusley",
        instructions="You're a helpful WhatsApp assistant...",
        tools=[{"type": "assistant"}],
        model="gpt-4-1106-preview",
        file_ids=[file.id] # type: ignore
    )
    return assistant

async def generate_response(message_body, wa_id, name):
    """Generate a response"""
    thread_id = check_if_thread_exists(wa_id)
    if thread_id is None:
        logging.info(f"Creating new thread for {name} with wa_id {wa_id}")
        thread = await client.beta.threads.create() # type: ignore
        store_thread(wa_id, thread.id)
        thread_id = thread.id
    else:
        logging.info(f"Retrieving existing thread for {name} with wa_id {wa_id}")
        thread = await client.beta.threads.retrieve(thread_id) # type: ignore

    message = await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body
    ) # type: ignore
    new_message = await run_assistant(thread, name) # type: ignore
    logging.info(f"To {name}: {new_message}")
    return new_message

async def run_assistant(thread):
    """Run the assistant"""
    assistant = await client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID) # type: ignore
    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    ) # type: ignore

    while run.status != "completed":
        await asyncio.sleep(0.5)
        run = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id) # type: ignore

    messages = await client.beta.threads.messages.list(thread_id=thread.id) # type: ignore
    new_message = messages.data[0].content[0].text.value
    logging.info(f"Generated message: {new_message}")
    return new_message

def check_if_thread_exists(wa_id):
    """Check if a thread exists"""
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)

def store_thread(wa_id, thread_id):
    """Store a thread"""
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id