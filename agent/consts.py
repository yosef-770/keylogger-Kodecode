import os

from dotenv import load_dotenv

load_dotenv()

# When the agent runs in production mode, it won't use the .env file, so BASE_URL is fixed value.
if os.getenv("ENV_MODE") == "development":
    API_BASE_URL = os.getenv("BASE_URL")
else:
    API_BASE_URL = "https://server-kodcode.droga.co.il"