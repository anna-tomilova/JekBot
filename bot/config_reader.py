import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    bot_token: str
    database_url: str
    starting_score: int = 1000
    spin_cost: int = 30

config = Settings()
