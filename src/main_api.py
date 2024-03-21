import math
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from src.gpt_controller import GPTController
from src.db_manager import DBManager
from src.session_manager import SessionManager
import sys
import asyncio
from src.firebase_auth import auth_user_token
from dotenv import load_dotenv
load_dotenv()
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError
from contextlib import asynccontextmanager

# prevents asyncio errors on Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class UserInput(BaseModel):
    user_token: str
    campaign_id: str
    content: str

class CharacterData(BaseModel):
    name: str
    background: str
    strength: str
    dexterity: str
    constitution: str
    intelligence: str
    wisdom: str
    charisma: str

class NewCampaignInput(BaseModel):
    user_token: str
    character_data: CharacterData

class UserTokenInput(BaseModel):
    user_token: str

class LoadCampaignInput(BaseModel):
    user_token: str
    campaign_id: str


database_uri = os.getenv("DATABASE_URL")  # or other relevant config var
if database_uri.startswith("postgres://"):
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)

db_manager = DBManager(database_uri)
gpt_controller = GPTController(os.getenv('OPENAI_API_KEY'))
session_manager = SessionManager()
scheduler = AsyncIOScheduler()

def credits_task():
    db_manager.check_and_giveaway_credits()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(credits_task, 'interval', minutes=60)
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)

# todo: implement CORS properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/fetch_campaigns/")
async def fetch_campaigns(input: UserTokenInput):
    # auth
    decoded_token = auth_user_token(input.user_token)
    if decoded_token is None:
        return
    try:
        # get user data
        print('fetching campaigns for:', decoded_token['uid'])
        user_session_ids = session_manager.filter_sessions_by_owner(decoded_token['uid'])
        session_names = session_manager.get_session_names(user_session_ids)
        session_player_names = session_manager.get_session_player_names(user_session_ids)
        session_player_levels = session_manager.get_session_player_levels(user_session_ids)
        user_sessions_info = []
        for i in range(len(user_session_ids)):
            user_sessions_info.append({
                "campaign_id": user_session_ids[i],
                "campaign_name": session_names[i],
                "player_name": session_player_names[i],
                "player_Level": session_player_levels[i]
            })
        return {"user_campaigns":  user_sessions_info, "maintenance_mode": False}
    except Exception as e:
        print('exception fetching user campaigns', e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/create_campaign/")
async def create_campaign(input: NewCampaignInput):
    # auth
    decoded_token = auth_user_token(input.user_token)
    if decoded_token is None: 
        return
    print('creating new campaign for', decoded_token['uid'])
    print('character data:', input.character_data)
    try:
        campaign_id = session_manager.create_session(decoded_token['uid'])
        # campaign_data = db_manager.create_campaign(decoded_token['uid'])
        session = session_manager.get_session(campaign_id)
        session.set_char_sheet(input.character_data.name, input.character_data.background, 
                             input.character_data.strength, input.character_data.dexterity, input.character_data.constitution, 
                             input.character_data.intelligence, input.character_data.wisdom, input.character_data.charisma)
        print('campaign_id:', campaign_id)
        return {'campaign_id': campaign_id}
    except Exception as e:
        print('exception create campaign', e)
        print('session was', session)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/load_campaign/")
async def load_campaign(input: LoadCampaignInput):
    # auth
    decoded_token = auth_user_token(input.user_token)
    if decoded_token is None: 
        return
    user_data = db_manager.get_or_create_user(decoded_token['uid'])
    # user_data = user_manager.get_or_create_user_data(decoded_token['uid'])
    try:
        session = session_manager.get_session(input.campaign_id)
        if session is None:
            print(f'user {decoded_token['uid']} request load_campaign failed: campaign_id {input.campaign_id} does not exist')
            return
        if session.owner != decoded_token['uid']:
            print(f'user {decoded_token['uid']} request load_campaign failed: does not have access to campaign_id {input.campaign_id}')
            return
        print('sending session data for', decoded_token['uid'])
        return {
            "messages": session.messages[1:], # ignore system msg
            "char_sheet": session.player_char_sheet.get_prompt(),
            "campaign_notes": session.campaign_notes.get_prompt(),
            "is_user_turn": session.user_turn,
            "credits": user_data.credits,
            "campaign_intro_img_b64": session.campaign_intro_img_b64str,
        }
    except Exception as e:
        print('exception loading campaign', e)
        raise HTTPException(status_code=500, detail="Internal server error")
        
@app.post("/process_input/")
async def process_input(input: UserInput):
    # auth
    decoded_token = auth_user_token(input.user_token)
    if decoded_token is None:
        return
    user_data = db_manager.get_or_create_user(decoded_token['uid'])
    # user_data = user_manager.get_or_create_user_data(decoded_token['uid'])
    try:
        session = session_manager.get_session(input.campaign_id)
        if session is None:
            print(f'user {decoded_token['uid']} request process_input failed: campaign_id {input.campaign_id} does not exist')
            return
        if session.owner != decoded_token['uid']:
            print(f'user {decoded_token['uid']} request process_input failed: does not have access to campaign_id {input.campaign_id}')
            return
        if user_data.credits < 0:
            return {
                "messages": session.messages[1:] + [{"role": "assistant", "content": "You don't have enough credits to play. Wait until tomorrow or buy more."}], # does not change the original messages
                "char_sheet": session.player_char_sheet.get_prompt(),
                "campaign_notes": session.campaign_notes.get_prompt(),
                "is_user_turn": session.user_turn,
                "credits": user_data.credits,
                "campaign_intro_img_b64": None
            }
        tick_resp = await session.tick_session(input.content, gpt_controller)
        user_data = db_manager.set_user_credits(decoded_token['uid'], user_data.credits - math.ceil(tick_resp['cost'] * 10))
        intro_img = None if len(session.messages) != 10 else session.campaign_intro_img_b64str # hack to send only when needed. Later we must change the api to only send the new info and not the whole state every time
        return {
            "messages": session.messages[1:], # ignore system msg
            "char_sheet": session.player_char_sheet.get_prompt(),
            "campaign_notes": session.campaign_notes.get_prompt(),
            "is_user_turn": session.user_turn,
            "credits": user_data.credits,
            "campaign_intro_img_b64": intro_img
        }
    except Exception as e:
        print('exception process_input', e)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/fetch_profile/")
async def fetch_profile(input: UserTokenInput):
    # auth
    decoded_token = auth_user_token(input.user_token)
    if decoded_token is None:
        return
    user_data = db_manager.get_or_create_user(decoded_token['uid'])
    acc_type = "undefined"
    if user_data.acc_type == 0:
        acc_type = "Normal"
    if user_data.acc_type == 1:
        acc_type = "VIP"
    return {
        "acc_type": acc_type,
        "credits": user_data.credits
    }

@app.get("/")
async def root():
    return {"message": "Hello to Auto D&D!"}
