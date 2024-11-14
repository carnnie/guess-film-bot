import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


class ImproperlyConfigured(Exception):
    """Raises when a environment variable is missing"""

    def __init__(self, variable_name, *args, **kwargs):
        self.variable_name = variable_name
        self.message = f"Set the {variable_name} environment variable."
        super().__init__(self.message, *args, **kwargs)


def get_env_variable(var_name: str, cast=str) -> str:
    """Get an environment variable or raise an exception.

    Args:
        var_name: a name of a environment variable.

    Returns:
        A value of the environment variable.

    Raises:
        ImproperlyConfigured: if the environment variable is not set.
    """

    try:
        return cast(os.environ[var_name])
    except KeyError:
        raise ImproperlyConfigured(var_name)
    except TypeError:
        raise TypeError(f"Variable {var_name} must be type {cast}.")


BASE_PATH: str = Path(__file__).resolve().parent.parent
RESOURCES_PATH: str = os.path.join(BASE_PATH, "res/")

BOT_TOKEN: str = get_env_variable("BOT_TOKEN")

''' Mongo settings '''
MONGO_HOST: str = get_env_variable("MONGO_HOST")
MONGO_PORT: str = get_env_variable("MONGO_PORT", int)
MONGO_USERNAME: str = get_env_variable("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD: str = get_env_variable("MONGO_INITDB_ROOT_PASSWORD")
MONGO_DATABASE: str = get_env_variable("MONGO_INITDB_DATABASE")
MONGO_CONNECTION_URI: str = (
    f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?retryWrites=true&w=majority&appName=Cluster0"
)

FILMS_FILE_PATH: str = os.path.join(RESOURCES_PATH, get_env_variable("FILMS_FILE_PATH"))