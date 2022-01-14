import instaloader
from utils.path import Path


class InstagramContext:
    __instance = None

    @staticmethod
    def get_context(username: str = None, password: str = None):
        if InstagramContext.__instance is None:
            InstagramContext.__instance = instaloader.Instaloader()

            if username is not None and password is not None:
                try:
                    InstagramContext.__instance.load_session_from_file(username,
                                                                       InstagramContext.get_session_path(username))
                except FileNotFoundError:
                    InstagramContext.__instance.context.log("Session file not found. Try to login.")

                if not InstagramContext.__instance.context.is_logged_in:
                    InstagramContext.__instance.login(username, password)
                    InstagramContext.__instance.save_session_to_file(InstagramContext.get_session_path(username))

        return InstagramContext.__instance

    @staticmethod
    def get_session_path(username: str):
        return Path.get_abs_path(f'instagram/session/session-{username}')
