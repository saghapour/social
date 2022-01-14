from instaloader import Profile
from utils.config_reader import Config
# from database.dbs import MongoDB
from .instagram_context import InstagramContext


class InstagramBase:
    def __init__(self):
        default_config = Config.read_conf('defaults')
        username = None
        password = None
        if default_config.instagram.has_key('username') and default_config.instagram.has_key('password'):
            username = default_config.instagram.username
            password = default_config.instagram.password

        self._context = InstagramContext.get_context(username, password)

    def get_profile(self, username: str) -> Profile:
        return Profile.from_username(self._context.context, username)

    def get_profile_collection_key(self, postfix: str = None):
        name = "instagram_profile"
        if postfix:
            name = f"{name}_{postfix}"
        return name
