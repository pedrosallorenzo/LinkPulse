import asyncio
import aiohttp
from database import SessionLocal
from models import Link

async def check_url(session, url):
    try:
        async with session.get(url, timeout=5) as resp:
            return resp.status == 200
    except:
        return False
    
async def monitor():
    while True:
        async with aiohttp.ClientSession() as session:
            db = SessionLocal()
            links = db.query(Link).all()
            for link in links:
                status = await check_url(session, link.url)
                link.status = "OK" if status else "OFFLINE"
                db.add(link)
            db.commit()
        await asyncio.sleep(300)