import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class EnvSchema(BaseModel):
    OPENAI_API_KEY: str = Field(None, min_length=1)
    LUMAAI_API_KEY: str = Field(None, min_length=1)
    CLOUDFLARE_R2_ACCESS_KEY_ID: str = Field(None, min_length=1)
    CLOUDFLARE_R2_ACCESS_KEY_SECRET: str = Field(None, min_length=1)
    CLOUDFLARE_ACCOUNT_ID: str = Field(None, min_length=1)
    
env = EnvSchema(
    OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY"),
    LUMAAI_API_KEY=os.environ.get("LUMAAI_API_KEY"),
    CLOUDFLARE_ACCOUNT_ID=os.environ.get("CLOUDFLARE_ACCOUNT_ID"),
    CLOUDFLARE_R2_ACCESS_KEY_ID=os.environ.get("CLOUDFLARE_R2_ACCESS_KEY_ID"),
    CLOUDFLARE_R2_ACCESS_KEY_SECRET=os.environ.get("CLOUDFLARE_R2_ACCESS_KEY_SECRET"),
)