from sqlmodel import Field, SQLModel
from datetime import datetime, UTC

class CronjobTimers(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    last_update: datetime = datetime.now(UTC)

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    uid: str
    acc_type: int = 0
    credits: int = 1000

class Campaign(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    owner: int = Field(foreign_key="user.id")
    name: str
    world_geography: str
    world_lore: str
    main_storyline: str
    messages_start_index: int = 1
    is_user_turn: bool = True

class GenStoryImg(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    # campaign_id: int = Field(foreign_key="campaign.id")
    campaign_id: int # to be made a FK later
    img_bytes: bytes
    prompt: str
    model: str
    cost: float
    campaign_msg_id: int

class City(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id")
    name: str
    description: str

class Faction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id")
    name: str
    description: str

class Sidequest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id")
    name: str
    description: str

class NPC(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id")
    name: str
    description: str

class CharSheet(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id")
    name: str = "Josh"
    race: str = "human"
    class_: str = "fighter"
    alignment: str = "neutral"
    background: str = "noble"
    level: int = 1
    experience: int = 0
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    health: int = 10
    ac: int = 10
    speed: int = 30

class CharItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    char_sheet_id: int = Field(foreign_key="charsheet.id")
    item_name: str
    quantity: int = 1
    description: str

class CharSkill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    char_sheet_id: int = Field(foreign_key="charsheet.id")
    skill_name: str
    level: int = 1

class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id")
    timestamp: str
    role: str
    content: str
    tool_call_id: str
    function_json: str

class MessagesResume(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaign.id")
    start_message_ind: int = 0
    end_message_ind: int = 0
    content: str
    prompt: str
    model: str
    cost: float
