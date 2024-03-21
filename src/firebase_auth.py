import os
from firebase_admin import credentials, auth
import firebase_admin
import json
from dotenv import load_dotenv
load_dotenv()

firebase_credentials = json.loads(os.getenv('FIREBASE_CREDENTIALS'))
firebase_app = firebase_admin.initialize_app(credentials.Certificate(firebase_credentials))

def auth_user_token(user_token):
    try:
        decoded_token = auth.verify_id_token(user_token, clock_skew_seconds=10)
        if decoded_token is None:
            print('Auth failed, could not decode token:', user_token)
        return decoded_token
    except Exception as e:
        print('exception on auth_user_token', e)
        return None
