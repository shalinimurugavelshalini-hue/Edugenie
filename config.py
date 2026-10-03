import os
from dotenv import load_dotenv


# Load variables from .env file
load_dotenv()


# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Gemini model
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


# Application settings
APP_NAME = os.getenv(
    "APP_NAME",
    "EduGenie"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0"
)


# Validate required configuration
def validate_config():
    """
    Check whether the required environment
    variables are available.
    """

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add it to the .env file."
        )


if __name__ == "__main__":
    try:
        validate_config()
        print("Configuration is valid.")
    except RuntimeError as error:
        print(f"Configuration error: {error}")