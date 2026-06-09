from common.auth.core import GenericJWTAuthentication
from common.auth.user_sync import directory_user_sync_service

class DirectoryJWTAuthentication(GenericJWTAuthentication):
    """
    Directory-specific JWT Authentication.
    Uses DirectoryUserSyncService to handle user registration/caching.
    """
    @property
    def sync_service(self):
        return directory_user_sync_service

JWTAuthentication = DirectoryJWTAuthentication
