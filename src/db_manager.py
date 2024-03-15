import os
import sys
from sqlmodel import Field, SQLModel, create_engine

class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    uid: str
    acc_type: int = 0
    credits: int = 1000

class Campaigns(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    owner: int = Field(foreign_key="users.id")
    name: str
    world_geography: str
    world_lore: str
    main_storyline: str
    messages_start_index: int = 1

class GenStoryImgs(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaigns.id")
    img_bytes: bytes
    prompt: str
    model: str
    cost: float
    campaign_msg_id: int

class Cities(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaigns.id")
    name: str
    description: str

class Factions(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaigns.id")
    name: str
    description: str

class Sidequests(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaigns.id")
    name: str
    description: str

class NPCs(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaigns.id")
    name: str
    description: str

class CharSheets(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaigns.id")
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

class CharItems(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    char_sheet_id: int = Field(foreign_key="charsheets.id")
    item_name: str
    quantity: int = 1
    description: str

class CharSkills(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    char_sheet_id: int = Field(foreign_key="charsheets.id")
    skill_name: str
    level: int = 1

class Messages(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaigns.id")
    timestamp: str
    role: str
    content: str
    tool_call_id: str
    function_json: str

class MessagesResumes(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    campaign_id: int = Field(foreign_key="campaigns.id")
    start_message_ind: int = 0
    end_message_ind: int = 0
    content: str
    prompt: str
    model: str
    cost: float

if __name__ == "__main__":
    DATABASE_URL = os.environ['DATABASE_URL']
    engine = create_engine(DATABASE_URL, echo=True)

    # create all defined tables not already in the database
    # SQLModel.metadata.create_all(engine)

    # drop all tables in the database
    # SQLModel.metadata.drop_all(engine)
    
    # drop a specific table
    SQLModel.metadata.tables['mymodel'].drop(engine)

    sys.exit()
