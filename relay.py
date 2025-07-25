import os, asyncio, json
from fastapi import FastAPI, Request
from discord import Intents
from discord.ext import commands

TOKEN      = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_ALERT_CHANNEL"))

intents = Intents.default()
bot     = commands.Bot(command_prefix="!", intents=intents)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start(TOKEN))

@app.post("/alert")
async def receive_alert(req: Request):
    data = await req.json()
    if isinstance(data, str):
        msg = data[:1900]
    else:
        msg = data.get("content", json.dumps(data))[:1900]
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(msg)
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "alive"}
