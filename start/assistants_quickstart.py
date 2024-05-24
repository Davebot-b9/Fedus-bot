import os
import shelve
#import asyncio
from dotenv import load_dotenv
from openai import OpenAI

from app.services.openai_service import (
    check_if_thread_exists,
    run_assistant,
    store_thread,
)

# Load environment variables
load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=OPEN_AI_API_KEY)


class AssistantsFedus:
    # @staticmethod
    # async def upload_file(path):
    #     """Upload a file with an "assistants" purpose"""
    #     file = await client.files.create(file=open(path, "rb"), purpose="assistants") # type: ignore
    #     return file

    # @staticmethod
    # async def create_assistant(file):
    #     """Create an assistant with the given file"""
    #     assistant = await client.beta.assistants.create(
    #         name="Fedus",
    #         instructions="Eres un asistente de WhatsApp útil que puede ayudar a las personas con cuestiones legales en Mexico. Utiliza tu base de conocimientos para responder mejor a las consultas de los clientes. Si no sabes la respuesta, di simplemente que no puedes ayudar con la pregunta y aconseja contactar directamente con el anfitrión. Sea serio y preciso.",
    #         tools=[{"type": "retrieval"}],
    #         model="gpt-4o-2024-05-13",
    #         file_ids=[file.id], # type: ignore
    #     )
    #     return assistant

    @staticmethod
    def check_if_thread_exists(wa_id):
        """Check if a thread exists for the given WhatsApp ID"""
        with shelve.open("threads_db") as threads_shelf:
            return threads_shelf.get(wa_id, None)

    @staticmethod
    def store_thread(wa_id, thread_id):
        """Store the thread ID for the given WhatsApp ID"""
        with shelve.open("threads_db", writeback=True) as threads_shelf:
            threads_shelf[wa_id] = thread_id

    @staticmethod
    def generate_response(message_body, wa_id, name):
        """Generate a response for the given message"""
        thread_id = check_if_thread_exists(wa_id)
        if thread_id is None:
            print(f"Creating new thread for {name} with wa_id {wa_id}")
            thread = client.beta.threads.create() # type: ignore
            store_thread(wa_id, thread.id)
            thread_id = thread.id
        else:
            print(f"Retrieving existing thread for {name} with wa_id {wa_id}")
            thread = client.beta.threads.retrieve(thread_id) # type: ignore

        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_body,
        ) # type: ignore
        new_message = run_assistant(thread)
        print(f"To {name}:", new_message)
        return new_message

    @staticmethod
    def run_assistant(thread):
        """Run the assistant on the given thread"""
        assistant = client.beta.assistants.retrieve(ASSISTANT_ID) # type: ignore
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        ) # type: ignore
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id) # type: ignore
        messages = client.beta.threads.messages.list(thread_id=thread.id) # type: ignore
        new_message = messages.data[0].content[0].text.value # type: ignore
        print(f"Generated message: {new_message}")
        return new_message


    new_message = generate_response("Que opciones tengo ante una multa por exceso de velocidad en la ciudad de mexico?", "123", "John")

    new_message = generate_response("Como puedo realizar una denuncia ante la presencia de violencia familiar?", "456", "Sarah")

    # new_message = generate_response("Que documentos necesito para poder hacer reclamo de una herencia?", "123", "John")

    # new_message = generate_response("Puedes proporcionarme los numero de emergencia ante violencia familiar en mexico?", "456", "Sarah")
