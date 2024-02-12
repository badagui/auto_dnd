# resumir chunks da transcrição

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from src.GPTController import GPTController
from dotenv import load_dotenv
from src.session_manager import SessionManager
load_dotenv()
import sys
import asyncio

# prevents asyncio errors on Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class UserInput(BaseModel):
    campaign_id: str
    content: str

class NewCharacterInput(BaseModel):
    campaign_id: str
    name: str
    background: str
    strength: str
    dexterity: str
    constitution: str
    intelligence: str
    wisdom: str
    charisma: str

class GetCampaignInput(BaseModel):
    campaign_id: str

app = FastAPI()

# todo: implement CORS properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gpt_controller = GPTController(os.getenv('OPENAI_API_KEY'))
session_manager = SessionManager()

@app.post("/load_campaign/")
async def load_campaign(input: GetCampaignInput):
    try:
        return {
            "response": {
                "has_started":  session_manager.check_session_exists(input.campaign_id),
            }
        }
    except Exception as e:
        print('exception loading campaign', e)
        raise HTTPException(status_code=500, detail="Internal server error")
        
@app.post("/create_character/")
async def create_character(input: NewCharacterInput):
    try:
        session = session_manager.get_or_create_session(input.campaign_id)
        session.set_char_sheet(input.name, input.background, 
                             input.strength, input.dexterity, input.constitution, 
                             input.intelligence, input.wisdom, input.charisma)
        return {} # frontend behavior solely based on response.ok (status code 200)
    except Exception as e:
        print('exception create character', e)
        raise HTTPException(status_code=500, detail="Internal server error")
    
@app.post("/process_input/")
async def process_input(input: UserInput):
    try:
        session = session_manager.get_or_create_session(input.campaign_id)
        
        if input.content == "[GET_SESSION_DATA]":
            return session.get_session_data()
        
        await session.get_gm_response(input.content, gpt_controller)
        return session.get_session_data()
    except Exception as e:
        print('exception process input', e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
async def root():
    return {"message": "Hello to Auto D&D!"}
