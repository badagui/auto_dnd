import io
from PIL import Image
import base64
import os
import sys
from sqlalchemy import MetaData
from sqlmodel import SQLModel, Session, create_engine, select
from src.db_models import CronjobTimers, User, Campaign, GenStoryImg, City, Faction, Sidequest, NPC, CharSheet
from datetime import datetime, UTC, timedelta
from src.gpt_controller import GPTController, GPTController_sync
from dotenv import load_dotenv
load_dotenv()

class DBManager():
    def __init__(self, DATABASE_URL, echo=False):
        self.engine = create_engine(DATABASE_URL, echo=echo)

    def reset_all_tables(self):
        # drop all tables from current engine
        metadata = MetaData()
        metadata.reflect(self.engine)
        metadata.drop_all(self.engine)
        # create tables defined by current SQLModel classes
        SQLModel.metadata.create_all(self.engine)

    def drop_table(self, table_name: str):
        # table_name is the name of the table in the database and must be linked to a SQLModel class
        SQLModel.metadata.tables[table_name].drop(self.engine)

    def create_user(self, uid: str):
        with Session(self.engine) as session:
            user = User(uid=uid)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def get_user(self, uid: str):
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.uid == uid)).first()
            return user
            # REMOVED: credit giving will be a cron job
            # if user:
                # print('user found', user.last_credit)
                # MAX_CREDITS = 1000
                # if user.credits < MAX_CREDITS and (datetime.now(UTC) - user.last_credit.replace(tzinfo=UTC)).min >= 1:
                #     elapsed_time = (datetime.now(UTC) - user.last_credit.replace(tzinfo=UTC))
                #     # find time difference in days rounded down
                #     print('elapsed_time', elapsed_time)
                #     print('elapsed days', elapsed_time.min)
                #     user.last_credit = datetime.now(UTC)
                # elapsed_time = (datetime.now(UTC) - user.last_credit.replace(tzinfo=UTC))
                # print('datetime current', datetime.now(UTC))
                # print('elapsed_time', elapsed_time)
                # print('difference', elapsed_time.days, elapsed_time.min)
                # print('difference', elapsed_time > timedelta(days=1))
    
    def delete_user(self, uid: str):
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.uid == uid)).first()
            if user:
                session.delete(user)
                session.commit()
                return True
            return False

    def get_or_create_user(self, uid: str):
        user = self.get_user(uid)
        if not user:
            print('creating user', uid)
            user = self.create_user(uid)
        return user
    
    def set_user_credits(self, uid: str, credits: int):
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.uid == uid)).first()
            if user:
                user.credits = credits
                session.commit()
                session.refresh(user)
                return user
            else:
                print(f'set_user_credits: user {uid} not found')
    
    def set_user_vip(self, uid: str, is_vip: bool):
        with Session(self.engine) as session:
            user = session.exec(select(User).where(User.uid == uid)).first()
            if user:
                user.acc_type = 1 if is_vip else 0
                session.commit()
                session.refresh(user)
                return user
            else:
                print(f'set_user_vip: user {uid} not found')
       
    def get_campaign(self, campaign_id: str):
        with Session(self.engine) as session:
            campaign = session.exec(select(Campaign).where(Campaign.id == campaign_id)).first()
            if not campaign:
                print(f'campaign {campaign_id} not found')
            return campaign
           
    # def create_campaign(self, owner_uid: str):
    #     with Session(self.engine) as session:
    #         campaign = Campaign()
    #         session.add(campaign)
    #         session.commit()
    #         session.refresh(campaign)
    #         return campaign
        
    def check_and_giveaway_credits(self):
        with Session(self.engine) as session:
            cron_timer = session.exec(select(CronjobTimers).where(CronjobTimers.name == 'credits_giveaway_job')).first()
            if not cron_timer:
                print('creating new credits_giveaway_job')
                cron_timer = CronjobTimers(name='credits_giveaway_job')
                session.add(cron_timer)
                session.commit()
                session.refresh(cron_timer)
            delta_time = datetime.now(UTC) - cron_timer.last_update.replace(tzinfo=UTC)
            delta_days = delta_time.total_seconds() / 60 / 60 / 24
            users = session.exec(select(User).where(User.credits < 1000)).all()
            if delta_days >= 1:
                print('giving away credits')
                # cron_timer.last_update = datetime.now(UTC)
                cron_timer.last_update = cron_timer.last_update + timedelta(days=1)
                session.add(cron_timer)
                for user in users:
                    if user.acc_type == 1:
                        user.credits += 500
                    else:
                        user.credits += 100
                    user.credits = user.credits if user.credits <= 1000 else 1000
                    session.add(user)
                session.commit()
            else:
                print('not enough time elapsed')

    def store_img(self, campaign_id: int, img_bytes: bytes, prompt: str, model: str, cost: float, campaign_msg_id: int):
        with Session(self.engine) as session:
            gen_story_img = GenStoryImg(campaign_id, img_bytes, prompt, model, cost, campaign_msg_id)
            session.add(gen_story_img)
            session.commit()
            session.refresh(gen_story_img)
            return gen_story_img
    
    def get_campaign_intro_img(self, campaign_id: int):
        with Session(self.engine) as session:
            gen_story_img = session.exec(select(GenStoryImg).where(GenStoryImg.campaign_id == campaign_id)).first()
            return gen_story_img

if __name__ == "__main__":
    DATABASE_URL = os.environ['DATABASE_URL']
    db_manager = DBManager(DATABASE_URL, echo=False)
    if len(sys.argv) > 1:

        if sys.argv[1] == 'reset_all_tables':
            assert len(sys.argv) == 2
            db_manager.reset_all_tables()
            print('reset all tables')

        elif sys.argv[1] == 'drop_table':
            assert len(sys.argv) == 3
            table_name = sys.argv[2]
            print('dropping table', table_name)
            db_manager.drop_table(table_name)

        elif sys.argv[1] == 'set_user_vip':
            assert len(sys.argv) == 4
            uid = sys.argv[2]
            is_vip = sys.argv[3] == 'true'
            print('setting user vip', uid, is_vip)
            db_manager.set_user_vip(uid, is_vip)

        elif sys.argv[1] == 'set_user_credits':
            assert len(sys.argv) == 4
            uid = sys.argv[2]
            credits = int(sys.argv[3])
            print(f'setting user credits', uid, credits)
            db_manager.set_user_credits(uid, credits)
        
        elif sys.argv[1] == 'giveaway_credits':
            assert len(sys.argv) == 2
            print('checking and giving away credits')
            db_manager.check_and_giveaway_credits()
        
        elif sys.argv[1] == 'store_img':
            assert len(sys.argv) == 2
            print('storing image in db')
            gpt_controller = GPTController_sync(os.getenv('OPENAI_API_KEY'))
            prompt = 'an astronaut sitted in a flamingo floater, floating through the universe and drinking a red can soda. Retro style.'
            resp = gpt_controller.send_img_query(prompt)
            image_data = base64.b64decode(resp['b64_json'])
            image_buffer = io.BytesIO(image_data) # file-like object
            optimized_buffer = io.BytesIO()
            image = Image.open(image_buffer)
            image.save(optimized_buffer, format='PNG', optimize=True)
            # b64 better to send in an API
            # optimized_image_b64 = base64.b64encode(optimized_buffer.getvalue()).decode('utf-8')
            # bytes is better to save in db
            # db_manager.store_img(1, optimized_buffer.getvalue(), prompt, "dall-e-3", 0.04, 1)
            # print('prompt:', prompt)
            # print('revised prompt:', resp['revised_prompt'])

    # db_manager.reset_all_tables()
    # test_user = db_manager.get_or_create_user("test_uid")
    # db_manager.get_user("test_uid")
    # db_manager.delete_user("test_uid")
    # print('test_user', test_user)
    # print('test_user', test_user.credits)
    # db_manager.set_user_credits("test_uid", 2000)
    # db_manager.create_campaign("test_uid")
    sys.exit()




    # def get_campaign(self, campaign_id: int):
    #     with Session(self.engine) as session:
    #         campaign = session.query(Campaigns).filter(Campaigns.id == campaign_id).first()
    #         return campaign

    # def create_gen_story_img(self, campaign_id: int, img_bytes: bytes, prompt: str, model: str, cost: float, campaign_msg_id: int):
    #     with Session(self.engine) as session:
    #         gen_story_img = GenStoryImgs(campaign_id=campaign_id, img_bytes=img_bytes, prompt=prompt, model=model, cost=cost, campaign_msg_id=campaign_msg_id)
    #         session.add(gen_story_img)
    #         session.commit()
    #         session.refresh(gen_story_img)
    #         return gen_story_img

    # def get_gen_story_img(self, gen_story_img_id: int):
    #     with Session(self.engine) as session:
    #         gen_story_img = session.query(GenStoryImgs).filter(GenStoryImgs.id == gen_story_img_id).first()
    #         return gen_story_img

    # def create_city(self, campaign_id: int, name: str, description: str):
    #     with Session(self.engine) as session:
    #         city = Cities(campaign_id=campaign_id, name=name, description=description)
    #         session.add(city)
    #         session.commit()
    #         session.refresh(city)
    #         return city

    # def get_city(self, city_id: int):
    #     with Session(self.engine) as session:
    #         city = session.query(Cities).filter(Cities.id == city_id).first()
    #         return city