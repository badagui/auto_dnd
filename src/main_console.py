from pydantic import BaseModel
import os
from src.GPTController import GPTController
from dotenv import load_dotenv
from src.session_manager import SessionManager
load_dotenv()
import sys
import asyncio

# prevents asyncio error on Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class UserInput(BaseModel):
    user_id: str
    content: str

gpt_controller = GPTController(os.getenv('OPENAI_API_KEY'))
session_manager = SessionManager()

async def process_input(input: UserInput):
    session = session_manager.create_session(input.user_id)
    if input.content == "[GET_SESSION_DATA]":
        return session.get_session_data()
    await session.tick_session(input.content, gpt_controller)
    return session.get_session_data()

def print_session_data_to_console(session_data):
    # header
    print(session_data['response']['campaign_notes'], end='\n')
    print(session_data['response']['char_sheet'], end='\n')
    # messages
    messages = session_data['response']['messages']
    for message in messages:
        message = dict(message)
        if message['role'] == "system":
            continue
        if message['content'] == "" or message['content'] == None:
            continue
        if message['role'] == "user":
            print(f"\033[92m{message['role']}: {message['content']}\033[0m") # bright green
        elif message['role'] == "tool":
            print(f"\033[93m{message['role']}: {message['content']}\033[0m") # bright yellow
        elif message['role'] == "assistant":
            print(f"\033[96m{('GM')}: {message['content']}\033[0m") # bright cyan
        else:
            print(f"{message['role']}: {message['content']}")

async def main():
    session = session_manager.create_session('userId')
    print_session_data_to_console(session.get_session_data())
    while True:
        system_ask = "user: " if session.user_turn else "press Enter to continue..."
        user_input = UserInput(user_id='userId', content=input(system_ask))
        session_data = await process_input(user_input)
        print_session_data_to_console(session_data)

def run():
    asyncio.run(main())
