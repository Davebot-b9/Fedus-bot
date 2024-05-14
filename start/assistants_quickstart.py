import os
import shelve
import time
import asyncio
from dotenv import load_dotenv
from openai import OpenAI

from app.services.openai_service import check_if_thread_exists, run_assistant, store_thread

# Load environment variables
load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)

class AssistantsFedus:
    # Upload file
    @staticmethod
    async def upload_file(path):
        # Upload a file with an "assistants" purpose
        file = await client.files.create(file=open(path, "rb"), purpose="assistants") # type: ignore
        return file

    # Create assistant
    @staticmethod
    async def create_assistant(file):
        assistant = await client.beta.assistants.create(
            name="Fedus",
            instructions="Bienvenido al Asistente Legal Fedus...",
            tools=[{"type": "retrieval"}],
            model="gpt-4-1106-preview",
            file_ids=[file.id], # type: ignore
        )
        return assistant
    
    @staticmethod
    # Thread management
    def check_if_thread_exists(wa_id):
        with shelve.open("threads_db") as threads_shelf:
            return threads_shelf.get(wa_id, None)

    @staticmethod
    def store_thread(wa_id, thread_id):
        with shelve.open("threads_db", writeback=True) as threads_shelf:
            threads_shelf[wa_id] = thread_id

    # Generate response
    @staticmethod
    async def generate_response(message_body, wa_id, name):
        thread_id = check_if_thread_exists(wa_id)
        if thread_id is None:
            print(f"Creating new thread for {name} with wa_id {wa_id}")
            thread = await client.beta.threads.create() # type: ignore
            store_thread(wa_id, thread.id)
            thread_id = thread.id
        else:
            print(f"Retrieving existing thread for {name} with wa_id {wa_id}")
            thread = await client.beta.threads.retrieve(thread_id) # type: ignore

        message = await client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_body,
        ) # type: ignore
        new_message = await run_assistant(thread) # type: ignore
        print(f"To {name}:", new_message)
        return new_message

    # Run assistant
    @staticmethod
    async def run_assistant(thread):
        assistant = await client.beta.assistants.retrieve("asst_7Wx2nQwoPWSf710jrdWTDlfE") # type: ignore
        run = await client.beta.threads.runs.create(
            thread_id=thread.id, # type: ignore
            assistant_id=assistant.id,
        ) # type: ignore
        while run.status != "completed":
            await asyncio.sleep(0.5)
            run = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id) # type: ignore
        messages = await client.beta.threads.messages.list(thread_id=thread.id) # type: ignore
        new_message = messages.data[0].content[0].text.value
        print(f"Generated message: {new_message}")
        return new_message
