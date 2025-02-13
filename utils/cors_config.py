import os
from config import MODE
from dotenv import load_dotenv

load_dotenv('.env')

def get_allowed_origins():
    mode = os.environ.get("MODE", "production")
    if mode == "local":
        return ["http://localhost:3030"]
    elif mode == "dev":
        return ["https://dev.pdf-analysis.moreel.me"]
    else:
        return ["https://pdf-analysis.moreel.me"]