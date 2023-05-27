from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get("api_key")
secret_key = os.environ.get("secret_key")