from elevenlabs import AsyncElevenLabs
from fastapi import APIRouter, HTTPException
import httpx

from src.env import env

elevenlabs_client = AsyncElevenLabs(api_key=env.ELEVENLABS_API_KEY)

router = APIRouter(prefix="/conversation", tags=["conversation"])

@router.post("/signed-url/")
async def create_signed_url():
    url = f"https://api.elevenlabs.io/v1/convai/conversation/get_signed_url?agent_id={env.ELEVENLABS_AGENT_ID}"
    
    headers = {
        "xi-api-key": env.ELEVENLABS_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get signed URL")
    
    body = response.json()
    return {"signed_url": body.get("signed_url")}
