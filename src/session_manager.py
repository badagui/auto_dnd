from src.campaign_notes import CampaignNotes
from src.player_char_sheet import PlayerCharSheet
from typing import Dict, List
from src.session_state import SessionState

# class UserData():
#     def __init__(self, uid: str):
#         # name, email, etc, are managed by firebase. We can fetch it using the uid.
#         self.uid = uid
    
# class UserManager():
#     def __init__(self):
#         self.user_data: Dict[str, UserData] = {} 

#     def get_or_create_user_data(self, uid: str):
#         if uid not in self.user_data:s
#             print('creating new user data for:', uid)
#             self.user_data[uid] = UserData(uid)
#         return self.user_data[uid]

class SessionManager():
    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}

    def create_session(self, owner_uid: str):
        # create a new session and return the session_id
        session_id = str(len(self.sessions))
        self.sessions[session_id] = SessionState(
            owner=owner_uid,
            player_char_sheet=PlayerCharSheet(),
            campaign_notes=CampaignNotes(),
            messages=[
                {"role": "system", "content": ""},
                {"role": "assistant", "content": "Welcome to our D&D 3.5 session. I'm here to help you with your campaign. Are we all set to embark on this extraordinary journey?"}
            ],
            user_turn=True
        )
        
        return session_id
    
    def filter_sessions_by_owner(self, owner_uid: str):
        # Find all sessions that belong to the specified owner - this will come from db in the future
        filtered_sessions = []
        for session_id, session_state in self.sessions.items():
            if session_state.owner == owner_uid:
                filtered_sessions.append(session_id)
        
        return filtered_sessions

    def get_session(self, session_id: str):
        if session_id not in self.sessions:
            print('session_id', session_id, 'not found')
            return None
        return self.sessions[session_id]

    def check_session_exists(self, session_id: str):
        return session_id in self.sessions
    
    def get_session_names(self, session_ids: List[str]):
        return [self.sessions[session_id].campaign_notes.campaign_name for session_id in session_ids]
    
    def get_session_player_names(self, session_ids: List[str]):
        return [self.sessions[session_id].player_char_sheet.name for session_id in session_ids]
        
    def get_session_player_levels(self, session_ids: List[str]):
        return [self.sessions[session_id].player_char_sheet.level for session_id in session_ids]