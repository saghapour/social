import os


class Path:
    @staticmethod
    def get_root_dir():
        return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    @staticmethod
    def get_abs_path(relative_path: str):
        return os.path.join(Path.get_root_dir(), relative_path)
