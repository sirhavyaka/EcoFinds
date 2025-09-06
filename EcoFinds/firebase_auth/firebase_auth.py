import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class FirebaseAuthentication:
    """
    Firebase authentication utility class
    """
    
    def __init__(self):
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """
        Initialize Firebase Admin SDK
        """
        if not firebase_admin._apps:
            try:
                # Try to get credentials from settings
                cred_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', None)
                if cred_path and cred_path.exists():
                    cred = credentials.Certificate(str(cred_path))
                    firebase_admin.initialize_app(cred)
                    logger.info("Firebase Admin SDK initialized with credentials file")
                else:
                    # Try to get from environment variable
                    import os
                    cred_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
                    if cred_json:
                        import json
                        cred_dict = json.loads(cred_json)
                        cred = credentials.Certificate(cred_dict)
                        firebase_admin.initialize_app(cred)
                        logger.info("Firebase Admin SDK initialized with environment credentials")
                    else:
                        # For development without credentials, just log a warning
                        logger.warning("Firebase Admin SDK not initialized - no credentials found")
                        logger.warning("Authentication will work on frontend but server-side verification will be limited")
                        return
            except Exception as e:
                logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
                logger.warning("Continuing without Firebase Admin SDK - frontend auth will still work")
    
    def verify_token(self, id_token):
        """
        Verify Firebase ID token and return decoded token
        """
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            return decoded_token
        except firebase_auth.InvalidIdTokenError:
            logger.warning("Invalid Firebase ID token")
            return None
        except firebase_auth.ExpiredIdTokenError:
            logger.warning("Expired Firebase ID token")
            return None
        except Exception as e:
            logger.error(f"Error verifying Firebase token: {str(e)}")
            return None
    
    def create_custom_token(self, uid, additional_claims=None):
        """
        Create custom token for a user
        """
        try:
            custom_token = firebase_auth.create_custom_token(uid, additional_claims)
            return custom_token.decode('utf-8')
        except Exception as e:
            logger.error(f"Error creating custom token: {str(e)}")
            return None
    
    def get_user(self, uid):
        """
        Get user data from Firebase
        """
        try:
            user_record = firebase_auth.get_user(uid)
            return user_record
        except firebase_auth.UserNotFoundError:
            logger.warning(f"User {uid} not found in Firebase")
            return None
        except Exception as e:
            logger.error(f"Error getting user from Firebase: {str(e)}")
            return None
    
    def delete_user(self, uid):
        """
        Delete user from Firebase
        """
        try:
            firebase_auth.delete_user(uid)
            return True
        except Exception as e:
            logger.error(f"Error deleting user from Firebase: {str(e)}")
            return False
